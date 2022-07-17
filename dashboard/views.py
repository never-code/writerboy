from cmath import log
from email import message
from itertools import count
from urllib.request import Request
from django.forms import ModelForm
from django.shortcuts import render, redirect
from django.contrib import messages
import time
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from numpy import empty
from requests import session

from .forms import *
from .models import *
from .functions import *


@login_required
def dashboard(request):
    emptyBlogs = []
    completedBlogs = []
    monthCount = 0
    blogs = Blog.objects.filter(profile=request.user.profile)
    for blog in blogs:
        sections = BlogSectionM.objects.filter(blog=blog)
        if sections.exists():
            blogWords = 0
            for section in sections:
                section.save()
                blogWords += int(section.wordCount)
                monthCount += int(section.wordCount)
            blog.wordCount = str(blogWords)
            blog.save()
            completedBlogs.append(blog)
        else:
            emptyBlogs.append(blog)
    context = {}
    context['numBlogs'] =  len(completedBlogs)
    context['monthCount'] = request.user.profile.monthlyCount
    context['countReset'] = '12 July 2022'
    context['emptyBlogs'] = emptyBlogs
    context['completedBlogs'] = completedBlogs
    context['allowance'] = checkCountAllowance(request.user.profile)
    return render(request, 'dashboard/main.html', context)

@login_required
def profile(request):
    context = {}

    if request.method == 'GET':
        form = ProfileForm(instance=request.user.profile, user = request.user)
        image_form  = ProfileImageForm(instance=request.user.profile)
        context['form'] = form
        context['image_form'] = image_form
        return render(request, 'dashboard/profile.html', context)

    if request.method == 'POST':

        form  =  ProfileForm(request.POST, instance = request.user.profile, user = request.user)
        image_form  = ProfileImageForm(request.POST, request.FILES, instance = request.user.profile)

        if form.is_valid():
            form.save()
            return redirect('profile')

        if image_form.is_valid():
           image_form.save()
           return redirect('profile')

    return render(request,'dashboard/profile.html', context)

@login_required
def blogTopic(request):
    context = {}
    if request.method == 'POST':
        blogIdea  = request.POST['blogIdea']
        request.session['blogIdea'] = blogIdea
        keywords  = request.POST['keywords']
        request.session['keywords'] = keywords

        audience  = request.POST['audience']
        request.session['audience'] = audience

        blogTopics = generateBlogTopicIdeas(blogIdea, audience, keywords)
        if len(blogTopics) > 0:
            request.session['blogTopics'] = blogTopics
            return redirect('blog-section')
        else:
            messages.error(request, "Oops we could not generate any blog ideas for you, please try again" )
            return redirect('blog-topic')
    return render(request, 'dashboard/blog-topic.html', context)


@login_required
def BlogSection(request):
    if 'blogTopics' in request.session:
        pass
    else:
        messages.error(request, "Start by creating blog topic ideas" )
        return redirect('blog-topic')

    context = {}
    context['blogTopics'] = request.session['blogTopics']
    return render(request, 'dashboard/blog-section.html', context)


@login_required

def deleteBlogTopic(request, uniqueId):
    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
        if blog.profile == request.user.profile:
            blog.delete()
            return redirect('main')
        else:
            messages.error(request, "Access Denied" )
            return redirect('main')
    except:
        messages.error(request, "Blog not found" )
        return redirect('main')





@login_required
def saveBlogTopic(request, blogTopic):

    if 'blogIdea' in request.session and 'keywords' in request.session and 'audience' in request.session and 'blogTopics' in request.session:
        blog = Blog.objects.create(
        title = blogTopic,
        blogIdea = request.session['blogIdea'],
        keyword =  request.session['keywords'],
        audience = request.session['audience'],
        profile = request.user.profile)
        blog.save()
        blogTopics = request.session['blogTopics']
        blogTopics.remove(blogTopic)
        request.session['blogTopics'] = blogTopics
        return redirect('blog-section')
    else:
        return redirect('blog-topic')

@login_required
def useBlogTopic(request, blogTopic):
    context = {}
    if request.method=='POST':
        for val in request.POST:
             if not 'csrfmiddlewaretoken' in val:
                prevBlog = ''
                bSections = BlogSectionM.objects.filter(blog=blog).order_by('date_created')
                for sec in bSections:
                    prevBlog += sec.title + '\n'
                    prevBlog += sec.body.replace('<br>', '\n')
                prevBlog = ''
                section = generateBlogSectionDetails(blogTopic, val, request.session['audience'], request.session['keywords'], request.user.profile)
                ##create database record
                blogSec = BlogSectionM.objects.create(
                title = val,
                body = section,
                blog = blog)
                blogSec.save()
                time.sleep(2)
        return redirect('view-generated-blog', slug = blog.slug)

        
    if 'blogIdea' in request.session and 'keywords' in request.session and 'audience' in request.session:
        blog = Blog.objects.create(
        title = blogTopic,
        blogIdea = request.session['blogIdea'],
        keyword =  request.session['keywords'],
        audience = request.session['audience'],
        profile = request.user.profile)
        blog.save()
        blogSections  = generateBlogSectionTitles(blogTopic, request.session['audience'], request.session['keywords'])
    else:
        return redirect('blog-topic')



    if len(blogSections)>0:
        request.session['blogSections'] = blogSections
        context['blogSections'] = blogSections
        
    else:
        messages.error(request, "Oops you beat the AI, please try again")
        return redirect('blog-topic')

    

    return render(request, 'dashboard/select-blog-sections.html', context)







@login_required
def createBlogFromTopic(request, uniqueId):
    context = {}
    try:
        blog = Blog.objects.get(uniqueId=uniqueId)
    except:
        messages.error(request, "Blog not found" )
        return redirect('main')
        
    blogSections  = generateBlogSectionTitles(blog.title, blog.audience, blog.keyword)
  



    if len(blogSections)>0:
        request.session['blogSections'] = blogSections
        context['blogSections'] = blogSections
        
    else:
        messages.error(request, "Oops you beat the AI, please try again")
        return redirect('blog-topic')

    if request.method=='POST':
        for val in request.POST:
             if not 'csrfmiddlewaretoken' in val:
                section = generateBlogSectionDetails(blog.title, val, blog.audience, blog.keyword, request.user.profile)
                ##create database record
                blogSec = BlogSectionM.objects.create(
                title = val,
                body = section,
                blog = blog)
                blogSec.save()
        return redirect('view-generated-blog', slug = blog.slug)

    return render(request, 'dashboard/select-blog-sections.html', context)






@login_required
def viewGeneratedBlog(request, slug):
    try:
        blog = Blog.objects.get(slug=slug)
    except:
        messages.error(request, "Something went wrong")
        return redirect('blog-topic')


    blogSections = BlogSectionM.objects.filter(blog = blog)
    context = {}
    context['blog'] = blog
    context['blogSections'] = blogSections

    return render(request, 'dashboard/view-generated-blog.html', context)


@login_required
def billing(request):
    context = {}
    return render(request, 'dashboard/billing.html', context )