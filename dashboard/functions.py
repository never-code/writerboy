from pydoc_data.topics import topics
from re import T
import openai
from django.conf import settings
openai.api_key = settings.OPENAI_API_KEY

def generateBlogTopicIdeas(topic, audience, keywords):
    blog_topics = []

    response = openai.Completion.create(
    model="text-davinci-002",
    prompt="Generate 6 blog topic ideas on the given topic: {}\nAudience:{}\nKeywords: {}\n*".format(topic, audience, keywords),
    temperature=0.8,
    max_tokens=300,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    if 'choices' in response: 
        if len (response ['choices'])>0: 
            res =  response ['choices'][0]['text'] 
        else:
            return []
    else:
        return []
    
    a_list = res.split('*')
    if len(a_list)>0:
        for blog in a_list:
            blog_topics.append(blog)
    else:
        return []
    return blog_topics



def generateBlogSectionTitles(topic, audience, keywords):
    blog_sections = []

    response = openai.Completion.create(
    model="text-davinci-002",
    prompt="Generate 8 blog section titles for the provided blog topic, audience and keywords: {}\nAudience:{}\nKeywords: {}\n*".format(topic, audience, keywords),
    temperature=0.8,
    max_tokens=300,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    if 'choices' in response: 
        if len (response ['choices'])>0: 
            res =  response ['choices'][0]['text'] 
        else:
            return []
    else:
        return []
    
    a_list = res.split('*')
    if len(a_list)>0:
        for blog in a_list:
            blog_sections.append(blog)
    else:
        return []
    return blog_sections







def generateBlogSectionDetails(blogTopic, sectionTopic, audience, keywords, profile):
    response = openai.Completion.create(
    model="text-davinci-002",
    prompt="Generate detailed blog section write up for the following blog section heading, using the blog title, audience and keywords provided.\nBlog Title: {} \nBlog Section Heading: {} \nAudience:{} \nKeywords: {} \n".format(blogTopic, sectionTopic, audience, keywords),
    temperature=0.8,
    max_tokens=500,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    if 'choices' in response: 
        if len (response ['choices'])>0: 
            res =  response ['choices'][0]['text'] 
            if not res == '':
                cleanedRes = res.replace('\n', '<br>')
                if profile.monthlyCount:
                    oldCount = int(profile.monthlyCount)
                else:
                    oldCount  = 0
            else:
                return ''
            oldCount += len(cleanedRes.split(' '))    
            profile.monthlyCount = str(oldCount)
            profile.save()
            return cleanedRes
        else:
            return ''
    else:
        return ''


def checkCountAllowance(profile):
    if profile.subscribed:
        type = profile.subscriptionType
        if type == 'free':
            max_limit = 5000
            if profile.monthlyCount:
                if int(profile.monthlyCount) < max_limit:
                    return True
                else:
                    return False
            else:
                return True

        elif type == 'starter':
            max_limit = 40000
            if profile.monthlyCount:
                if int(profile.monthlyCount) < max_limit:
                    return True
                else:
                    return False
            else:
                return True
        elif type == 'advanced':
            return True
        else:
            return False    

    else:
        max_limit = 5000
        if profile.monthlyCount:
            if int(profile.monthlyCount) < max_limit:
                return True
            else:
                return False
        else:
            return True






