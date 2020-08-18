from django.urls import path
from QMS.views import common
from QMS.views import auditorlist
from QMS.views import auditschedule
from QMS.views import empdetails
from QMS.views import workmanual
from QMS.views import auditcomment
from QMS.views import project_teamwise



app_name = 'QMS'


urlpatterns = [
    # path('cmt/',auditcomment.cmt,name='cmt'),

    path('homepage/',common.HomePage.as_view(),name='homepage' ),


    path('audittypeview/',common.AudittypeListview.as_view(),name='audittypeview' ),
    path('audittypecreate/',common.AudittypeCreate.as_view(),name='audittypecreate' ),
    path('audittypeupdate/<int:pk>/',common.AudittypeUpdate.as_view(),name='audittypeupdate'),
    path('audittypedelete/<int:pk>/',common.AudittypeDelete.ObjectDelete,name='audittypedelete' ),


    path('emppositionview/',common.EmployePositionListview.as_view(),name='emppositionview' ),
    path('emppositionform/',common.EmployePositionCreate.as_view(),name='emppositionform' ),
    path('emppositionupdate/<int:pk>/',common.EmployePositionUpdate.as_view(),name='emppositionupdate'),
    path('emppositiondelete/<int:pk>/',common.EmployePositionDelete.ObjectDelete,name='emppositiondelete' ),


    path('employedeptview/',common.EmployeDepartmentListview.as_view(),name='employedeptview' ),
    path('employedeptform/',common.EmployeDepartmentCreate.as_view(),name='employedeptform' ),
    path('employedeptupdate/<int:pk>/',common.EmployeDepartmentUpdate.as_view(),name='employedeptupdate'),
    path('employedeptdelete/<int:pk>/',common.EmployeDepartmentDelete.ObjectDelete,name='employedeptdelete' ),


    path('auditorlistform/',auditorlist.AuditorlistCreate.as_view(),name='auditorlistform'),
    path('auditorlistview/',auditorlist.AuditorlistListview.as_view(),name='auditorlistview'),
    path('auditorlistdelete/<int:pk>/',auditorlist.AuditorlistDelete.ObjectDelete,name='auditorlistdelete'),


    path('projectcreate/',project_teamwise.ProjectCreate.as_view(),name='projectcreate'),
    path('projectupdate/<int:pk>/',project_teamwise.ProjectUpdate.as_view(),name='projectupdate'),
    path('projectview/',project_teamwise.ProjectListview.as_view(),name='projectview'),
    path('projectdelete/<int:pk>/',project_teamwise.ProjectDelete.ObjectDelete,name='projectdelete'),
    path('teamwisecreate/',project_teamwise.TeamwiseCreate.as_view(),name='teamwisecreate'),
    path('teamwiseupdate/<int:pk>/',project_teamwise.TeamwiseUpdate.as_view(),name='teamwiseupdate'),
    path('teamwiseview/',project_teamwise.TeamwiseListview.as_view(),name='teamwiseview'),
    path('teamwisedelete/<int:pk>/',project_teamwise.TeamwiseDelete.ObjectDelete,name='teamwisedelete'),


    path('auditeeautocomplete/',auditschedule.ajax_response,name='auditeeautocomplete'),
    path('projectautocomplete/',auditschedule.ajax_hidden,name='projectautocomplete'),
    path('auditscheduleform/',auditschedule.AuditscheduleCreate.as_view(),name='auditscheduleform'),
    path('mrconfirmschedule/',auditschedule.MRconfirm.as_view(),name='mrconfirmschedule'),
    path('mrconfirmmail/',auditschedule.MRconfirm.Sendmail,name='mrconfirmmail'),
    path('auditscheduleview/',auditschedule.AuditscheduleListview.as_view(),name='auditscheduleview'),
    path('auditscheduleconfirmview/<int:pk>/',auditschedule.AuditscheduleConfirmListview.as_view(),name='auditscheduleconfirmview'),
                                            # passing string from template using url
    path(r'^confirmingmanagers/(?:(?P<manager_name>.+)/)?$',auditschedule.AuditscheduleConfirmListview.save,name="confirmingmanagers"),
    path('auditscheduleupdate/<int:pk>/',auditschedule.AuditscheduleUpdate.as_view(),name='auditscheduleupdate'),
    path('auditscheduledelete/<int:pk>/',auditschedule.AuditscheduleDelete.ObjectDelete,name='auditscheduledelete'),
    path('auditschedulepostpondcreate/<int:pk>/',auditschedule.AuditschedulePostpond.as_view(),name='auditschedulepostpondcreate'),
    path('auditschedulepostpondupdate/<int:pk>/',auditschedule.AuditschedulePostpondUpdate.as_view(),name='auditschedulepostpondupdate'),
    path('auditschedulecancel/<int:pk>/',auditschedule.AuditscheduleCancel.as_view(),name='auditschedulecancel'),
    path('auditscheduleclosed/<int:id>/',auditschedule.AuditscheduleClosed,name='auditscheduleclosed'),
    path('auditschedulereporttable/',auditschedule.AuditscheduleExportTable.as_view(),name='auditschedulereporttable'),
    path('auditschedulereport/',auditschedule.AuditscheduleExportTable.export,name='auditschedulereport'),
    path('ncrreporttable/',auditschedule.NCRExportTable.as_view(),name='ncrreporttable'),
    path('ncrreport/',auditschedule.NCRExportTable.export,name='ncrreport'),
    path('projectreporttable/',auditschedule.ProjectExportTable.as_view(),name='projectreporttable'),
    path('projectreport/',auditschedule.ProjectExportTable.export,name='projectreport'),
    path('ncrlogreporttable/',auditschedule.NCRLogExportTable.as_view(),name='ncrlogreporttable'),
    path('ncrlogreport/',auditschedule.NCRLogExportTable.export,name='ncrlogreport'),


    path('auditorcommentform/<int:pk>/',auditcomment.AuditorcommentCreate.as_view(),name='auditorcommentform'),
    path('sendmailauditor/<int:id>/',auditcomment.AuditorcommentCreate.Sendmail,name='sendmailauditor'),
    path('auditorcommentview/<int:pk>/',auditcomment.MrcommentListCreate.as_view(),name='auditorcommentview'),
    path('sendmailmr/<int:id>/',auditcomment.MrcommentListCreate.Sendmail,name='sendmailmr'),
    path('auditeecommentform/<int:pk>/',auditcomment.AuditeecommentCreate.as_view(),name='auditeecommentform'),
    path('sendmailauditee/<int:id>/',auditcomment.AuditeecommentCreate.Sendmail,name='sendmailauditee'),
    path('verifycommentform/<int:pk>/',auditcomment.VerifycommentCreate.as_view(),name='verifycommentform'),
    path('verifyajax/',auditcomment.load_page,name='verifyajax'),
    path('sendmailverify/<int:id>/',auditcomment.VerifycommentCreate.Sendmail,name='sendmailverify'),


    path('empdetailsform/',empdetails.EmployeeDetailsCreate.as_view(),name='empdetailsform'),
    path('empdetailsview/',empdetails.EmployeeDetailsListview.as_view(),name='empdetailsview'),
    path('empdetailsupdate/<int:pk>/',empdetails.EmployeeDetailsUpdate.as_view(),name='empdetailsupdate'),
    path('empdetailsdelete/<int:pk>/',empdetails.EmployeeDetailsDelete.ObjectDelete,name='empdetailsdelete'),


    path('workmanualform/',workmanual.WorkManualCreate.as_view(),name='workmanualform'),
    path('workmanualview/',workmanual.WorkManualListview.as_view(),name='workmanualview'),
    path('workmanualupdate/<int:pk>/',workmanual.WorkManualUpdate.as_view(),name='workmanualupdate'),
    path('workmanualdelete/<int:pk>/',workmanual.WorkManuaDelete.ObjectDelete,name='workmanualdelete'),
    path('workmanualaddnew/<int:pk>/',workmanual.WorkManualaddnewCreate.as_view(),name='workmanualaddnew'),

   ]
