import pytest
from reports.models import IncidentReport
from organisations.models import Organisation
from content.models import EducationContent, Quiz
from users.models import User


@pytest.mark.django_db
def test_incident_report_creation():
    report = IncidentReport.objects.create(
        abuse_type='physical',
        relationship='self',
        county='Nairobi',
        sub_county='Westlands',
        sms_ref_code='TST00001',
    )
    assert report.county == 'Nairobi'
    assert report.flagged_for_review == False
    assert report.urgency_score is None


@pytest.mark.django_db
def test_organisation_unverified_by_default():
    org = Organisation.objects.create(
        name='Test NGO',
        description='Test description',
        services='counselling',
        county='Nairobi',
    )
    assert org.verified == False


@pytest.mark.django_db
def test_user_default_role_is_public():
    user = User.objects.create_user(
        username='testuser',
        email='test@test.com',
        password='Test@1234',
    )
    assert user.role == User.Role.PUBLIC
    assert user.is_org_staff() == False
    assert user.is_platform_admin() == False


@pytest.mark.django_db
def test_education_content_not_approved_by_default():
    org = Organisation.objects.create(
        name='Test Org',
        description='Test',
        services='legal aid',
        county='Mombasa',
    )
    content = EducationContent.objects.create(
        title='Test Article',
        body='Test body',
        format='article',
        topic='legal',
        organisation=org,
    )
    assert content.approved == False


@pytest.mark.django_db
def test_quiz_completion_count_starts_at_zero():
    org = Organisation.objects.create(
        name='Quiz Org',
        description='Test',
        services='education',
        county='Kisumu',
    )
    quiz = Quiz.objects.create(
        title='Test Quiz',
        topic='recognise',
        organisation=org,
        questions=[],
    )
    assert quiz.completion_count == 0
