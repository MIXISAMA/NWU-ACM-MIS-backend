import smtplib

from django.core.mail import send_mail
from django.contrib import admin
from django.shortcuts import HttpResponseRedirect

from NWU_ACM_MIS import settings
from member.models import Member
from plan.models import Plan

mail_content_template = '''
我们发布了一个新的计划: {}

计划时间: 
    开始: {}
    结束: {}

以下是详细信息:
{}

欢迎参加,
{}
'''


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'typ', 'clock_in', 'clock_out', 'has_sent')
    ordering = ('-clock_in',)
    add_fieldsets = (
        (None, {'fields': (
            'name',
            'typ',
            'detail',
            'clock_in',
            'clock_out',
        )}),
    )
    fieldsets = add_fieldsets + (
        ('邮件通知', {'fields': (
            'members',
            'has_sent',
        )}),
    )
    
    readonly_fields = ('has_sent',)
    autocomplete_fields = ('members',)

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def response_change(self, request, obj:Plan):
        if '_addallads' in request.POST:
            obj.save()
            obj.members.add(*Member.objects.filter(role=Member.Role.AD))
            self.message_user(request, '添加了所有的现役队员')
            return HttpResponseRedirect('.')
        if '_addallnovices' in request.POST:
            obj.save()
            obj.members.add(*Member.objects.filter(role=Member.Role.NOVICE))
            self.message_user(request, '添加了所有的萌新队员')
            return HttpResponseRedirect('.')
        if '_sendemail' in request.POST:
            obj.has_sent = True
            obj.save()
            failed_members = []
            mail_content = mail_content_template.format(
                obj.name, obj.clock_in, obj.clock_out, obj.detail,
                settings.PROJECT_VERBOSE_NAME
            )
            for member in obj.members.all():
                try:
                    send_mail(
                        obj.name,
                        f'您好，{member.realname}' + mail_content,
                        settings.EMAIL_FROM,
                        recipient_list=[member.user.email, ],
                        fail_silently=False,
                    )
                except smtplib.SMTPException:
                    failed_members.append(member)
            message = '己发送邮件'
            if failed_members:
                message += f', 其中给{failed_members}发送时失败'
            self.message_user(request, message)
            return HttpResponseRedirect('.')
        return super().response_change(request, obj)
