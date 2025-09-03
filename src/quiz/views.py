from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Exam, Question, Choice
from .forms import ExamForm, QuestionForm, ChoiceFormSet

# Lista de exámenes
def exam_list(request):
    exams = Exam.objects.all().order_by('-created_date')
    return render(request, 'quiz/exam_list.html', {'exams': exams})

# Detalle de un examen con sus preguntas
def exam_detail(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    questions = exam.questions.all().prefetch_related('choices')
    return render(request, 'quiz/exam_detail.html', {'exam': exam, 'questions': questions})

# Crear un examen
def exam_create(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save()
            messages.success(request, 'Examen creado correctamente.')
            return redirect('question_create', exam_id=exam.id)
    else:
        form = ExamForm()
    return render(request, 'quiz/exam_form.html', {'form': form})

# Añadir preguntas y opciones a un examen
def question_create(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST)

        if question_form.is_valid() and formset.is_valid():
            with transaction.atomic():
                question = question_form.save(commit=False)
                question.exam = exam
                question.save()
                formset.instance = question
                formset.save()

                # Validar que haya exactamente una opción correcta
                correct_count = question.choices.filter(is_correct=True).count()
                if correct_count != 1:
                    messages.warning(request, 'Debe haber exactamente una respuesta correcta.')
                else:
                    messages.success(request, 'Pregunta añadida correctamente.')

                # Decidir redirección
                if 'add_another' in request.POST:
                    return redirect('question_create', exam_id=exam.id)
                else:
                    return redirect('exam_detail', exam_id=exam.id)
    else:
        question_form = QuestionForm()
        formset = ChoiceFormSet()

    return render(request, 'quiz/question_form.html', {
        'exam': exam,
        'question_form': question_form,
        'formset': formset,
    })
