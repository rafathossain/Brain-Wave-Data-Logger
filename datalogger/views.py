from django.shortcuts import render, redirect
from .models import ExcelUpload, DataLog
from .forms import ExcelUploadForm
import pandas as pd
import os
from django.http import JsonResponse
from dateutil.parser import parse


# Homepage
def index(request):
    excel_form = ExcelUploadForm()
    dataFrame = []

    if request.method == 'POST':
        excel_form = ExcelUploadForm(request.POST, request.FILES)
        file_path = ''

        if excel_form.is_valid():
            instance = excel_form.save()
            file_path = instance.excel.path

        df = pd.read_excel(r'%s' % file_path)
        for key, row in df.iterrows():
            rows = []
            for col in range(0, len(row)):
                rows.append(str(row[col]))

            if rows[0] != 'nan' and rows[1] != 'nan':
                dataFrame.append(rows)

        dataFrame.pop(0)

        for rIndex, row in enumerate(dataFrame):
            for cIndex, col in enumerate(row):
                if col == 'nan':
                    dataFrame[rIndex][cIndex] = ''

        # print(dataFrame)

        if os.path.exists(file_path):
            os.remove(file_path)

        for rIndex, row in enumerate(dataFrame):
            data_stream = ''
            for cIndex, col in enumerate(row):
                if cIndex == 0:
                    data_stream += str(dataFrame[rIndex][cIndex])
                else:
                    data_stream += ',' + str(dataFrame[rIndex][cIndex])
            DataLog.objects.create(
                data_str=data_stream,
                item_count=str(len(data_stream.split(','))),
                index=rIndex
            )
            # break
        DataLog.objects.update(total=len(DataLog.objects.all()))

        return redirect('datalogger.log')

    context = {
        'excel_form': excel_form,
    }

    return render(request, 'datalogger/index.html', context)


def log(request):
    return render(request, 'datalogger/log.html')


def logData(request):
    search_value = request.GET['search[value]'].strip()
    print(search_value)
    startLimit = int(request.GET['start'])
    endLimit = startLimit + int(request.GET['length'])
    range_list = []
    for i in range(startLimit+1, endLimit+1):
        range_list.append(i)
    print(range_list)
    # print(startLimit)
    # print(endLimit)
    data_array = []

    totalLength = 0
    filterLength = 0

    if search_value != '':
        dataList = DataLog.objects.filter(data_str__contains=search_value).order_by('id')
        dataFilter = dataList[:10]
        # dataFilter = dataList
        if len(dataList) > 0:
            totalLength = dataList[0].total
        filterLength = len(dataList)
    else:
        dataList = DataLog.objects.filter(index__in=range_list).order_by('id')
        # print(len(dataList))
        # dataFilter = dataList[startLimit:endLimit]
        dataFilter = dataList
        if len(dataList) > 0:
            totalLength = dataList[0].total
            filterLength = dataList[0].total

    # print(dataList)

    for item in dataFilter:
        row_array = item.data_str.split(',')
        dateTime = parse(row_array[len(row_array) - 1]).strftime("%b %d, %Y %I:%M:%S %p")
        row_array = row_array[:-1]
        row_array[len(row_array) - 1] = dateTime
        data_array.append(row_array)

    # for j in range(startLimit, endLimit):
    #     row_array = []
    #     for i in range(0, 23):
    #         row_text = "<b>Row</b>" + str(j) + " Column" + str(i)
    #         row_array.append(row_text)
    #
    #     data_array.append(row_array)

    response = {
        "draw": request.GET['draw'],
        "recordsTotal": totalLength,
        "recordsFiltered": filterLength,
        "data": data_array
    }

    return JsonResponse(response)


def logOld(request):
    data_array = []
    dataFilter = DataLog.objects.all().order_by('id')
    for item in dataFilter:
        row_array = item.data_str.split(',')
        dateTime = parse(row_array[len(row_array) - 1]).strftime("%b %d, %Y %I:%M:%S %p")
        row_array = row_array[:-1]
        row_array[len(row_array) - 1] = dateTime
        data_array.append(row_array)

    context = {
        'data_array': data_array
    }

    return render(request, 'datalogger/log_slow.html', context)


def logDelete(request):
    DataLog.objects.all().delete()
    return redirect('datalogger.home')


def charts(request):
    limit = request.GET['limit']

    dataList = DataLog.objects.all().order_by('-id')
    dataList = dataList[:int(limit)]

    data = []
    set_a = []
    set_b = []

    for item in dataList:
        data_str = item.data_str.split(',')
        temp_array_a = [data_str[22][:10], data_str[1]]
        temp_array_b = [data_str[22][:10], data_str[2]]

        set_a.append(temp_array_a)
        set_b.append(temp_array_b)

    data.append(set_a)
    data.append(set_b)

    context = {
        'data': data
    }
    return render(request, 'datalogger/graph.html', context)
