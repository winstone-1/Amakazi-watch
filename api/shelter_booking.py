class ShelterBooking(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    organisation = models.ForeignKey('organisations.Organisation', on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(null=True)
    status = models.CharField(max_length=20)
    is_anonymous = models.BooleanField(default=True)

# Endpoint: POST /api/shelter/booking/request/
# Survivors can book shelter beds directly
