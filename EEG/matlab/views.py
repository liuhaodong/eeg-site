
CONF_THRESH = 52

def predictConfusion(start_time, end_time):
    atts = Attention.objects.filter(start_time__lte=end_time).filter(end_time__gte=start_time)
    if len(atts) == 0:
        return 0

    sum_att = 0.0
    for att in atts:
        sum_att += att.attention
    avg_att = sum_att / len(atts)
    print 'ATTENTION', avg_att
    if avg_att >= CONF_THRESH:
        return 1
    return 0

def trainMatlab(request):
    out = matlab.train()
    return HttpResponse(out)

def testMatlab(request):
    out = matlab.test('05_Feb_2014_15_49_47')
    return HttpResponse(out)

