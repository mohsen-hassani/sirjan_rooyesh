from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, get_object_or_404
from django.views import generic
from .models import Week, Question, UserAnswer, Choice, WeeklyAnswer
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum,Q
from django.db import connection

# Create your views here.

class WeekView(generic.ListView):
    def get_queryset(self):
        return Week.objects.all()
    template_name = 'week.html'
    context_object_name = 'week'

def index(request):
    weekly_scores = show_weekly_scores()
    return render(request, 'index.html',{'week_list': Week.objects.all(),'scores' : weekly_scores})

def week(request, id):
    context = Week.objects.get(pk=id)
    return render(request,'week.html',{'week':context,'questions':context.question_set.all()})

def login_page(request):
    return render(request, 'login.html', {})

def do_login(request):
    auth = authenticate(username=request.POST['username'], password=request.POST['password'])
    if auth is not None:
        login(request, auth)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request,'login.html',{'error_message':'نام کاربری یا رمز وارد شده اشتباه است!'})

def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def panel(request):
    if(request.user.is_authenticated):
        weeks = Week.objects.all()
        return render(request, 'panel.html', {
            'user':request.user,
            'weeks': weeks
            })
    else:
        return HttpResponseRedirect(reverse('login'))


def answer(request, id):
    if(request.user.is_authenticated):
        questions = Question.objects.filter(week = id)
        week = Week.objects.get(pk=id)
        user_answers = UserAnswer.objects.filter(week=week, user=request.user)
        return render(request, 'answer.html', {
            'user':request.user,
            'week':week,
            'questions': questions,
            'answers': user_answers
            })
    else:
        return HttpResponseRedirect(reverse('login'))


def blog(request, content):
    context = {}
    title = ''
    if(content == 'rules'):
        title = 'قوانین  مسابقه'

        context['مقدمه'] = {'1':'دانشجوی محترم ، این راهنما برای آشنایی شما با قوانین مسابقه‌ی هفتگی رویش با نام اختصاری (مهر) تدوین شده است. لطفاً برای آشنایی با قوانین و مقررات مسابقه، این متن رابا دقت  تا انتها مطالعه کنید.',
                        '2':'سری جدید مسابقه هفتگی رویش( طرح مهر)به دو صورت حضوری و مجازی برگزار خواهد شد ؛ به این معنا که سوالات مسابقه در پایگاه اطلاع رسانی  نهاد نمایندگی مقام معظم رهبری و  جایگاه مشخص شده در ساختمان کلاس ها بارگزاری شده و شرکت کنندگان در مسابقه باید پاسخ سوالات  را در سایت مذکور و در قسمت مربوطه وارد نمایند.',
                        '3':'دانشجویان عزیز توجه داشته باشند که لازم است جهت ثبت نام در سامانه؛ پاسخ سوالات  اولین هفته شرکت خود در طرح مهر را به صورت حضوری تحویل دفتر نهاد نمایندگی مقام معظم رهبری دهند و از هفته های بعد تنها با مراجعه این سایت پاسخ سوالات را در سامانه ثبت نمایند',
                        '4':'',
                        '5':'مسابقه ، هفت هفته غیر متوالی برگزار خواهد شد که در هر هفته 7 سوال تستی (به استثنای هفته آخرکه هشت سوال طرح شده ) بر روی سایت قرار خواهد گرفت ؛ بنابر این در مجموع دانشجویان شرکت کننده باید به 50 سوال تستی پاسخ دهند.',
                        '6':'شنبه  هر هفته ، سوالات بر روی سایت نهاد رهبری و جایگاه مشخص شده در ساختمان کلاس ها، قرار می گیرد که دانشجویان شرکت کننده در مسابقه، موظفند تا پایان ساعت اداری روز چهارشنبه همان هفته ، پاسخ  سوالات را در سایت نهاد قرار دهند.'}

        context['مدت زمان مسابقه'] = {'1':'مسابقه به مدت 7 هفته غیرمتوالی ادامه پیدا می کند'}

        context['مخاطبین مسابقه']:{
'مخاطبین این طرح دانشجویان دانشگاه صنعتی می باشند.'}

        context['امتیاز دهی'] = {
'1':
'نحوه ی امتیاز دهی بدین صورت می باشد که هر پاسخِ درست 2 امتیاز و هر پاسخ نادرست نیم نمره منفی دارد.'}

        context['جوایز هفتگی'] = {'1':'یکشنبه هر  هفته  پس از تصحیح پاسخنامه ها ومشخص شدن نفرات برترِ هفته قبل، جوایزهفتگی به صورت نقدی در مسجد دانشگاه بین نماز ظهر و عصر (در صورتی که امتیاز ها برابر باشد قرعه کشی صورت می گیرد) به نفرات برتر اهدا می گردد.','2':'','3':'نفر اول  : 300,000 ریال','4':'نفردوم :  250,000 ریال','5':'نفرسوم :  200,000  ریال','6':'','7':'لازم به ذکر است جوایز هفتگی تنها به افراد شرکت کننده در هفته قبل تعلق می گیرد و تجمیع امتیازات هفتگی تنها مربوط به جوایز ویژه پایان طرح می باشد.'}



        context['مناطق امن سه گانه']:{
            '1':'مسابقه رویش برای دانشجویان شرکت کننده در مسیر رسیدن به جوایز ویژه، سه منقطه امن در نظر گرفته است؛ به این معنا که وقتی شرکت‌کننده به امتیاز آن منقطه می‌رسد، جایزه مربوط به آن منقطه امن را به صورت قطعی دریافت خواهد کرد.',
            '2':'',
            '3':'منطقه امن اول: دانشجویان که مجموع امتیازات آنها به 80 برسد (اگر جز برندگان ویژه نباشند) وارد این منطقه امن شده اند وجایزه مربوط به آن را دریافت خواهند کرد',
            '4':'منطقه امن دوم: دانشجویان که مجموع امتیازات آنها به 90 برسد (اگر جز برندگان ویژه نباشند) وارد این منطقه امن شده اند وجایزه مربوط به آن را دریافت خواهند کرد.',
            '5':'منطقه امن سوم: دانشجویان که مجموع امتیازات هفت هفته آنها به95 برسد (اگر جز برندگان ویژه نباشند) وارد این منطقه امن شده اند وجایزه مربوط به آن را دریافت خواهند کرد.',
            '6':'',
            '7':'شرکت کنندگان تنها جایزه مربوط به یک منطقه را دربافت می کنند'}

        context['جوایز']:{
            '1':'علاوه بر جوایز هفتگی نقدی، هر هفته امتیازات جمع آوری شده و در پایان هفته هفتمِ طرح، جوایز نفیسی به شرح ذیل اهدا می گردد:',
            '2':'',
            '3':'نفر اول :       000  / 000 /10  ریال  وجه نقد',
            '4':'نفر دوم :    اسکان سه شبانه روز در مشهد مقدس با دو نفر همراهی( فقط شامل اسکان و غذا می باشد و ایاب و ذهاب بر عهده خود شخص می باشد)',
            '5':'نفر سوم  :   مبلغ  000/000/3 ریال وجه نقد',
            '6':'نفر چهارم :  مبلغ  000/000/2 ریال وجه نقد',
            '7':'نفر پنجم :  مبلغ  000/000/1 ریال وجه نقد',
            '8':'',
            '9':'ورود به منطقه امن اول : یک هفته غذای رایگان سلف',
            '10':'ورود به منطقه امن دوم : مبلغ  000 / 500  ریال وجه نقد',
            '11':'ورود به منطقه امن سوم : مبلغ  000/000/1 ریال وجه نقد',
            '12':'',
            '13':'برندگان جوایز ویژه  از بین فاتحین منطقه  امن دوم و سوم – یعنی کسانی که حداقل امتیاز 90 را کسب کرده باشند _ به قید قرعه انتخاب می شوند  بدیهی است افرادی که امتیاز بالاتری نسبت به هم منطقه ای خود کسب کرده اند از تعداد شانس بیشتری در قرعه کشی برخوردارند'}

        context['نحوه تقسیم شانس'] = {
            '1':'توضیح نحوه تقسیم شانس بین نفرات برتر جهت دریافت جوایز ویژه',
            '2':'',
            '3':'افرادی که مجموع امتیازات آنها در پایان طرح بین 90 الی 91.5 باشد دارای یک شانس در قرعه کشی هستند',
            '4':'افرادی که مجموع امتیازات آنها در پایان طرح بین 92 الی 93.5 باشد دارای دو شانس در قرعه کشی هستند',
            '5':'افرادی که مجموع امتیازات آنها در پایان طرح بین 94 الی 95.5 باشد دارای سه شانس در قرعه کشی هستند',
            '6':'افرادی که مجموع امتیازات آنها در پایان طرح بین 96 الی 97.5 باشد دارای چهار شانس در قرعه کشی هستند',
            '7':'افرادی که مجموع امتیازات آنها در پایان طرح بین 98 الی 100 باشد دارای پنچ شانس در قرعه کشی هستند'}

    elif (content == 'guide'):
        title = 'راهنمای استفاده از سایت'

        context['ثبت نام و ورود به سایت'] = {
            '1':'برای شرکت در مسابقه ابتدا باید در سایت ثبت نام شوید. جهت ثبت نام به دفتر نهاد رهبری دانشگاه مراجعه نمایید. پس از ثبت نام بر روی گزینه ورود در قسمت بالایی سایت کلیک کنید. در صفحه جدید اطلاعات خود را وارد کنید تا وارد سایت شوید.',
            '2':'اطلاعات ورود شما به سامانه در ادامه آمده است'}

        context['پاسخگویی به سوالات'] = {
            '1':'پس از ثبت نام از بین هفته ها هفته مورد نظر را انتخاب کرده و  بر روی گزینه شرکت در مسابقه کلیک کنید. (در صورتی که مهلت پاسخگویی به هفته ای تمام شده باشد امکان شرکت در آن هفته وجود نخواهد داشت)',
            '2':'سپس جواب های مورد نظر خود را علامت زده و دکمه ارسال را کلیک کنید. در صورتی که نمیخواهید به سوالی پاسخ دهید پاسخ آن سوال را خالی گذاشته و هیچ گزینه ای را انتخاب نکنید.',
            '3':'در صورتی که میخواهید پاسخ های ارسالی خود را مشاهده کرده و یا تغییر دهید هفته مورد نظر را انتخاب کرده و مجددا گزینه شرکت در مسابقه را انتخاب کنید. (تغییر پاسخ های ارسالی در صورتی امکان دارد که مهلت پاسخ گویی آن هفته نگذشته باشد)'}

        context['اطلاعات ورود به سامانه'] = {
            '1':'نام کاربری: شماره دانشجویی',
            '2':'رمز عبور: کد ملی'}

        # context['فراموشی رمز عبور'] = {
            # '۱':'در صورتی که رمز عبور خود را فراموش کرده اید به دفتر نهاد رهبری مراجعه کنید'}

    else:
        context['']='چنین صفحه ای وجود ندارد'
        title = 'اخطار'

    return render(request, 'blog.html', {
            'content':context,
            'blog_title':title
            })



def do_answer(request, week_id):
    week = get_object_or_404(Week ,pk=week_id)
    if(week_expired(week.id)):
        return render(request, 'message.html', {'message':'مهلت پاسخ دهی به این هفته تمام شده است'})
    else:
        if(request.user.is_authenticated):
            user = request.user
            qs = week.question_set.all()
            save_user_answers(user,week,qs, request.POST)
            return HttpResponseRedirect(reverse('answer',args=[week_id]))
        else:
            return HttpResponseRedirect(reverse('login'))


def week_expired(id):
    week = get_object_or_404(Week ,pk=id)
    if week.expired:
        return True
    else:
        return False

def save_user_answers(user, week, qs, post):
    for q in qs:
        ch_id = post.get(str(q.id), 0)
        user_answer_exists = UserAnswer.objects.filter(question=q, user=user).exists()
        if user_answer_exists:
            user_answer = UserAnswer.objects.filter(question=q, user=user)[0]
            if ch_id == 0:
                ch = None
            else:
                ch = Choice.objects.get(pk=ch_id)
            user_answer.choice = ch
            user_answer.save()
        else:
            if ch_id == 0:
                ch = None
            else:
                ch = Choice.objects.get(pk=ch_id)
            UserAnswer.objects.create(user=user, week=week,question=q, choice=ch)



def calculate_users_score():
    users_answer = UserAnswer.objects.all()
    for answer in users_answer:
        choice = answer.choice
        if choice is None:
            answer.score = 0
        elif choice.is_answer:
            answer.score = 2
        else:
            answer.score = -0.5
        answer.save()

def calculate_users_week_score(week):
    users_answer = UserAnswer.objects.filter(week=week)
    for answer in users_answer:
        choice = answer.choice
        if choice is None:
            answer.score = 0
        elif choice.is_answer:
            answer.score = 2
        else:
            answer.score = -0.5
        answer.save()

def calculate_user_score(user):
    user_answer = UserAnswer.objects.filter(user=user)
    for answer in user_answer:
        choice = answer.choice
        if choice is None:
            answer.score = 0
        elif choice.is_answer:
            answer.score = 2
        else:
            answer.score = -0.5
        answer.save()




def save_scores_to_weekly_table():
    cursor = connection.cursor()
    try:
        cursor.callproc('nahadsirjan$rooyeshdb.save_result_to_weekly_table', [])
        result_set = cursor.fetchall()
    finally:
        cursor.close()


def show_all_scores():
    cursor = connection.cursor()
    try:
        cursor.callproc('rooyesh_temp.users_total_score', [])
        result_set = cursor.fetchall()
    finally:
        cursor.close()
    scores = []
    for r in result_set:
        dic = {}
        dic['id'] = r[0]
        dic['un'] = r[1]
        dic['sc'] = r[2]
        scores.append(dic)
    return scores

def show_weekly_scores():
    scores = WeeklyAnswer.objects.filter(~Q(user_id=1) & ~Q(user_id=2) & ~Q(user_id=97)).order_by('-all_weeks')
    return scores