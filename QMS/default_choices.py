"""Employee Details form Choices"""

employ_status = (
        ('','---Select---'),
        (0,'Active'),
        (1,'Inactive'),
        (2,'Hold'),
        (3,'Settlement')
    )

#""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"""Audit_comments form Choices"""

status = (
    ('','--- Select ---'),
    (0,'C'),
    (1,'OFI'),
    (2,'NC')
)


auditeechoice = (
    (0,'In Progress'),
    (1,'Completed'),
 )


verifychoice = (
    (0,'Yet-verify'),
    (1,'Re-submit'),
    (2,'Verified'),
 )


mr_choice = (
 (0,'To Review'),
 (1,'Clarified'),
 (2,'Accepted'),
)


  # '""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""'

"""WorkManual form Choices"""


type = (
    ('Project','Project'),
    ('Tender','Tender')
    )



    # """"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


"""Project Details Form"""

type = (
    (1,'Project'),
    (2,'Tender')
)
project_status=(
    (0,'Active'),
    (1,'Inactive'),
    (2,'Hold'),
    (3,'Cancelled')
)



# """""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""



"""AuditSchdule Model"""

audit_comment_status = (
        (0,'Yet to start'),
        (1,'Auditor and Auditee to Respond'),
        (2,'Auditor to Respond'),
        (3,'Auditee to Respond'),
        (4,'Auditor to Verify'),
        (5,'MR to Respond'),
        (6,'Waiting for Closed'),
        (7,'Completed')
)
