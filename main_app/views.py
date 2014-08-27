import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render
from django.core.mail import send_mail
import stripe
from instagram.client import InstagramAPI
import local_settings
from main_app.models import Profile, StripeKey


def home(request):
    return render(request, "home.html")

def get_api_access(access_token=None):
    api = InstagramAPI(client_id=local_settings.client_id, client_secret=local_settings.client_secret,
                       redirect_uri="http://localhost:8000/thank-you", access_token=access_token)
    return api


@csrf_exempt
def thank_you(request):
    if request.method == "POST":
        account = Profile.objects.get(access_token=Profile.objects.filter()[0].access_token)#instagram_id=54989816) # bullshit hack
        account.email = request.POST["email"]
        account.save()
        return render(request, "how_it_works.html", locals())
    else:
        code = request.GET.get('code')
        print "This is the code: {}".format(code)
        api = get_api_access()
        access_token = api.exchange_code_for_access_token(code)
        user = Profile.objects.get_or_create(access_token=access_token[0],
                                           bio=access_token[1]["bio"], website=access_token[1]["website"],
                                           profile_picture=access_token[1]["profile_picture"],
                                           full_name=access_token[1]["full_name"], instagram_id=access_token[1]["id"],
                                           user=access_token[1]["username"])[0]
        user.save()
        user = Profile.objects.get(access_token=access_token[0])
        return render(request, "thank-you.html", {"user": user})


def all_tagged_for_sale(request):
    api = get_api_access()
    for_sale = api.tag_recent_media(10, 5, tag_name="forsale")
    media = for_sale[0]
    return render(request, "for-sale.html", locals())


def vendogram_mentions(request):
    api = get_api_access()
    for_sale = api.tag_recent_media(10, 5, tag_name="vendogram")
    media = for_sale[0]
    return render(request, "vendogram-mentions.html", locals())


def my_media(request):
    api = get_api_access(access_token=Profile.objects.filter()[0].access_token)
    my_media = api.user_recent_media()
    media = my_media[0]
    return render(request, "my-media.html", locals())


def following_selling(request):
    api = get_api_access(access_token=Profile.objects.filter()[0].access_token)
    my_media = api.user_media_feed()
    media = my_media[0]
    return render(request, "following.html", locals())


def post_email(request):
    account = Profile.objects.get(access_token=Profile.objects.filter()[0].access_token)#instagram_id=54989816) # bullshit hack
    account.email = request.GET.get('mail')
    return render(request, "email.html")


def stripe_connect(request):
    url = "https://connect.stripe.com/oauth/token"
    client_secret = local_settings.stripe_secret
    code = str(request.GET['code'])
    grant_type = 'authorization_code'
    query_args = {'client_secret': client_secret, 'code': code, 'grant_type': grant_type}
    r = requests.post(url, data=query_args)
    StripeKey.objects.create(
        api_key=r.json()['access_token'],
        user=request.user
    )

    # Creating a Recipient
    stripe.Recipient.create(
        name=request.user.first_name,
        description=request.user.email,
        type='individual',
        api_key=r.json()['access_token']
    )

    # Creating user as a customer as well
    stripe.Customer.create(
        description=request.user.email,
        api_key=r.json()['access_token']
    )

    return render(request, "stripe_connect.html")


def how_it_works(request):
    return render(request, "how_it_works.html")


def get_access_token():
    return HttpResponse("cool!")


def check_if_media_is_for_sale(photos):
    for_sale_items = []
    for item in photos:
        if "buy" in item.caption.text.lower():
            for_sale_items.append(item)
    return for_sale_items


def media_has_comments(for_sale_items):
    commented_items =[]
    for item in for_sale_items:
        commented_items.append(item)
    return commented_items


def email_buyer(buyer_email):
    message = "Invoice"
    from_email ="armenlsuny@gmail.com"
    send_mail("Checkout with Vendogram", message, from_email, [buyer_email], fail_silently=False)


def comment_is_bought(commented_items):
    # checks text comment to see if contains the text 'buy'
    # returns a list of comments with word buy in them
    # should talk to seller's media django object, and say sold or inventoy -= 1
    for item in commented_items:
        if "bought" in item["data"]["text"]:
            buyer_id = item["data"]["from"]["id"]
            email_buyer(buyer_id)


def commentor_is_registered():
    # see if commentor's user_name/id is registered with us
    # if not pop from array
    pass


def send_commentor_invoice():
    # later to include imporved stripe
    pass


# BackEnd Work Flow
def add_media_to_inventory():
    #save media info as a django object
    # will use check_if_media_is_for_sale
    pass


def both_emails_purchase(media):
    seller_subject = "{}, someone bought your thing!".format(Profile.objects.filter()[0].full_name)
    seller_message = "{}, Someone bought your thing! And this is a message"
    buyer_subject = "Here's an invoice for thee thing you bought"
    buyer_message = "Now pay the person for the thing which you bought, this is a message"
    from_email ="armenlsuny@gmail.com"
    email = Profile.objects.filter()[0].email
    for item in media:
        if item.comments:
            for com in item.comments:
                if "Bought".lower() in com.text.lower():
                    buyer_name = "{}".format(com).split()[1]
                    guy = Profile.objects.filter()[0]
                    send_mail("{} here's an invoice for thee thing you bought".format(buyer_name), buyer_message, from_email, ["tran.william26@gmail.com"],
                              fail_silently=False)
                    send_mail(seller_subject, seller_message, from_email, [email],
                              fail_silently=False)


def sold(request):
    api = get_api_access(access_token=Profile.objects.filter()[0].access_token)
    my_media = api.user_recent_media()
    media = my_media[0]
    both_emails_purchase(media)
    return render(request, "sold.html", locals())


def armen(request):
    return render(request, "armen.html")


# helper for bellow...
def get_locations(recent_media):
    for picture in recent_media:
        print picture


# This is even more in development than the code above
# it is a raw and ugly, ugly way of finding out from where a given piece of media on IG's 'likers' are from.
# currently it gets 1 lat-long from 1 post of 1 liker of 1 piece of media.
def likes_from(request):
    # give access to api
    api = get_api_access(access_token=Profile.objects.filter()[0].access_token)
    user_media = api.user_recent_media()
    quin = user_media[0][0].likes[0]
    quin_id = user_media[0][0].likes[0].id
    print "this for sure is quin:"
    print quin_id
    print dir(quin)
    print quin.full_name
    print "the above is for sure quin\n\n "
    print dir(quin)
    print dir(api.user_recent_media(user_id=quin_id)[0][0])
    print api.user_recent_media(user_id=quin_id)[0][0].location.point
    print "latitide: {}".format(api.user_recent_media(user_id=quin_id)[0][0].location.point.latitude)
    print "latitide: {}".format(api.user_recent_media(user_id=quin_id)[0][0].location.point.longitude).split()
    return render(request, 'likes.html', locals())
