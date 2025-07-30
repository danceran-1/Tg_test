from django.shortcuts import render, redirect
from django.views.decorators.cache import never_cache
from .forms import RegistrationForm
from .models import User
from .forms import CriterionForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import os,json
import bcrypt 
import pandas as pd
import matplotlib.pyplot as plt
import csv
from django.http import HttpResponse
import matplotlib

matplotlib.use('Agg')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class WelcomeMessageView(APIView):
    def get(self, request):
        return Response({"message": "Добро пожаловать в API"})

def index(request):
    return render(request, 'main/index.html')


def password_check(request,password,loggin,spesial_password):

       
            
        if str(password).strip() == str(spesial_password).strip():
            success_message = f"Авторизация для {loggin} выполнена успешно"
            request.session['is_special'] = True
            return redirect('success')

        else:
            error_message = f'Неверный пароль{password}!={spesial_password}'
            return render(request, 'main/index.html',
                    {'form': RegistrationForm(), 'error_message': error_message})
            
        


def index(request):
    """Авторизация"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        with connection.cursor() as cursor:

            # тут обычных
            cursor.execute(
                "SELECT username,telegram_id FROM users WHERE username = %s",
                [username]
            )
            user_data = cursor.fetchone()

            if user_data:
                return password_check(request, password,user_data[0],user_data[1])

            else:
                error_message = 'Пользователь не найден'
                return render(request, 'main/index.html', 
                           {'form': RegistrationForm(), 'error_message': error_message})

    else:
        return render(request, 'main/index.html', {'form': RegistrationForm()})

def registr(request):
    error_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            error_message = 'Пароли не совпадают'
            return render(request, 'main/registr.html', 
                        {'error_message': error_message})
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT username WHERE username =%s",
                    [username]
                )
            us_name = cursor.fetchone()

            if us_name == "":
                error_message = 'Нет такого tg_id'
                return render(request, 'main/registr.html', 
                        {'error_message': error_message})

        except Exception as e:
            error_message = f"Ошибка при регистрации: {str(e)}"
        try:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            hashed_password_str = hashed_password.decode('utf-8')

            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, user_password) VALUES (%s, %s)",
                    [username, hashed_password_str]
                )
            
            return redirect("success") 
        
        except Exception as e:
            error_message = f"Ошибка при регистрации: {str(e)}"
    
    return render(request, 'main/registr.html', {'error_message': error_message})

def get_two_weeks_report(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Получаем данные за последние 2 недели
        weeks = list(data.keys())[-2:]
        result = {}

        for week in weeks:
            week_data = data[week]
            result[week] = {
                'dates': [day['date'] for day in week_data],
                'avg_temps': [day['avg_temperature'] for day in week_data],
                'avg_humidity': [day['avg_humidity'] for day in week_data],
                'min_water': [day['min_water_level'] for day in week_data]
            }

            result[week]['zipped'] = list(zip(
                result[week]['dates'],
                result[week]['avg_temps'],
                result[week]['avg_humidity'],
                result[week]['min_water']
            ))

        return result

    except Exception as e:
        return f"Ошибка: {str(e)}"


def graphic(df):

    plt.figure(figsize=(10, 5))
    plt.plot(df['time'], df['temperature'], label='Температура (°C)', marker='o', color='tomato')
    plt.plot(df['time'], df['humidity'], label='Влажность (%)', marker='s', color='skyblue')
    plt.plot(df['time'], df['water_level'], label='Уровень воды (л)', marker='^', color='green')

    plt.title("Дневной график")
    plt.xlabel("Время")
    plt.ylabel("Значение")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    output_path = os.path.join("static", 'graphs', 'daily_plot.png')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()

def daily_report(file_path):

    try: 
        with open(file_path, 'r') as file:
            df = json.load(file)
        today = "2025-07-28"

        if today in df:

            report_df = pd.DataFrame(df[today])
            
            graphic(report_df)

            report = f"📊 Дневной отчёт за {today}\n\n"
            report += f"🌡 Средняя температура: {report_df['temperature'].mean():.1f}°C\n"
            report += f"💧 Средняя влажность: {report_df['humidity'].mean():.1f}%\n"
            report += f"⚠️ Средний уровень воды: {report_df['water_level'].mean():.1f} литров\n"
            report += f"\n📈 Максимальная температура: {report_df['temperature'].max():.1f}°C\n"
            report += f"📉 Минимальная влажность: {report_df['humidity'].min():.1f}%\n"

        else:
            return "нет данных"
        return report
    
    except Exception as e:
        return f"Ошибка генерации отчёта: {e}"

def currient(file_path):

    try:
        with open(file_path, 'r') as file:
                json_data = json.load(file)
            
        status_df = pd.DataFrame([json_data['greenhouse_status']])
            
        

        return {
            'status_df': status_df,
            'temperature': status_df['temperature'][0],
            'humidity': status_df['humidity'][0],
            'water_level': status_df['water_level'][0]
        }
    
    except FileNotFoundError as e:
        print(f"Ошибка: Файл {file_path} не найден")
        raise
    except json.JSONDecodeError as e:
        print(f"Ошибка: Некорректный JSON в файле {file_path}")
        raise
    except KeyError as e:
        print(f"Ошибка: Отсутствует ключ {e} в JSON-структуре")
        raise
    except Exception as e:
        print(f"Неожиданная ошибка при чтении файла: {e}")
        raise

def download_csv(request):

    file_path_current = os.path.join(settings.STATIC_ROOT, 'info', 'daily_report.json')
    
    try:
        with open(file_path_current, 'r') as file:
            json_data = json.load(file)
            
        today = "2025-07-28"

        status_df = pd.DataFrame(json_data[today])
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="greenhouse_data.csv"'
        status_df.to_csv(path_or_buf=response, index=False)
        
        return response
    
    except Exception as e:
        return HttpResponse(f"Ошибка при генерации CSV: {e}", status=500)

@never_cache
def success(request):
    user_id = 5083058662  # пока фиксированный пользователь
    row = get_info_db(user_id)
    
    file_path_current = os.path.join(settings.STATIC_ROOT, 'info', 'greenhouse_data.json')
    current_data = currient(file_path_current)

    file_path_daily = os.path.join(settings.STATIC_ROOT, 'info', 'daily_report.json')
    daily_data  = daily_report(file_path_daily)

    file_path_weekly = os.path.join(settings.STATIC_ROOT, 'info', 'weekly_report.json')
    weekly_data = get_two_weeks_report(file_path_weekly)

    context = {
        'status_df': current_data['status_df'],
        'daily_report': daily_data,
        'weekly_report': weekly_data,
        'fan_on': row[2],
        'water_on': row[1],
    }
    return render(request, 'main/success.html', context)


def get_info_db(user_id):
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM device_states WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
    
    return row

# @never_cache
# def report_page(request):
    
#     user_id = 5083058662  # пока фиксированный пользователь
#     row = get_info_db(user_id)
    
#     print(f"report_page: fan_on={row[2]}, water_on={row[1]}")
#     context = {
#         'fan_on': row[2],
#         'water_on': row[1],
#     }
#     return render(request, 'main/success.html', context)


@csrf_exempt
def turn_fan_on(request):
    if request.method == 'POST':
        print("dsda")
        user_id = 5083058662
        with connection.cursor() as cursor:
            cursor.execute("UPDATE device_states SET fan_on = NOT fan_on WHERE user_id = %s", (user_id,))
    return redirect('success')

@csrf_exempt
def turn_water_on(request):
    if request.method == 'POST':
        user_id = 5083058662
        with connection.cursor() as cursor:
            cursor.execute("UPDATE device_states SET water_on = NOT water_on WHERE user_id = %s", (user_id,))
    return redirect('success')

def success1(request):
    if request.method == 'POST':
        if 'A' in request.POST and 'B' in request.POST:
            A = request.POST.get('A')
            B = request.POST.get('B')

            if A is not None and B is not None:
                try:
                    A = int(A)
                    B = int(B)

                    K1 = (A / B) * 100
                    result = f"К1 = {K1:.2f}%"
                    mark = 0
                    if 55 < K1 <= 59:
                        mark = 1
                    elif 60 < K1 <= 64:
                        mark = 3
                    elif 65 < K1 <= 70:
                        mark = 5

                except (ValueError, ZeroDivisionError):
                    result = "Ошибка ввода данных. Пожалуйста, введите числовые значения для A и B."
                    mark = 0
            else:
                result = "Пожалуйста, введите значения для A и B."
                mark = 0

            return render(request, 'main/success.html', {'result': result, 'mark': mark})

        elif 'A1' in request.POST and 'B1' in request.POST:
            A1 = request.POST.get('A1')
            B1 = request.POST.get('B1')

            if A1 is not None and B1 is not None:
                try:
                    A1 = int(A1)
                    B1 = int(B1)

                    K2 = (A1 / B1) * 100
                    result2 = f"К2 = {K2:.2f}%"
                    mark1 = 0
                    if 45 < K2 <= 49:
                        mark1 = 1
                    elif 50 < K2 <= 54:
                        mark1 = 3
                    elif 55 < K2 <= 60:
                        mark1 = 5

                except (ValueError, ZeroDivisionError):
                    result2 = "Ошибка ввода данных. Пожалуйста, введите числовые значения для A1 и B1."
                    mark1 = 0
            else:
                result2 = "Пожалуйста, введите значения для A1 и B1."
                mark1 = 0

            return render(request, 'main/success.html', {'result2': result2, 'mark1': mark1})

    return render(request, 'main/success.html')

def criterion_view(request):
    if request.method == 'POST':
        form = CriterionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = CriterionForm()
    return render(request, 'main/criterion.html', {'form': form})

def media(request):
    media_root = settings.MEDIA_ROOT
    files = os.listdir(media_root)
    return render(request, 'main/media.html', {'files': files})