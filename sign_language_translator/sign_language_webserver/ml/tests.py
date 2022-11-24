from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile

import mock
import shutil
import tempfile
import datetime

from .forms import EvaluationForm
from .models import *

# Create your tests here.
MEDIA_ROOT = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class Test_ML_Model(TestCase):
    def setUp(self):
        # print("\t>>>>>> TEST_ML_MODEL SETUP <<<<<<")
        for i in range(3):
            test_title = f'test_model{i+1}'
            test_mock = mock.MagicMock(spec=File)
            test_mock.name = f'test_model{i+1}.h5'
            ML_Model.objects.create(title=test_title, model_file=test_mock)
        # print("\t>>>>>> TEST_ML_MODEL SETUP <<<<<<")

    @classmethod
    def tearDownClass(cls):
        def tearDownClass(cls):
            shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
            super().tearDownClass()

    def test_create_모델(self):
        test = ML_Model.objects.get(title='test_model1')
        self.assertEqual(test.title, 'test_model1')
        self.assertEqual(test.version, 1.0)
        self.assertEqual(test.date_published, datetime.date.today())
        self.assertEqual(len(ML_Model.objects.all()), 3)

    def test_update_모델버전(self):
        # print(">> test_update_모델버전")
        test = ML_Model.objects.get(title='test_model1')
        old_version = test.version
        test.version = 1.2
        test.save()

        test = ML_Model.objects.get(title='test_model1')
        self.assertNotEqual(test.version, old_version)

    def test_update_모델선택(self):
        # print(">> test_udpate_model_version")
        model = ML_Model.objects.get(pk=1)
        model.is_selected = True
        model.save()#update_fields=['is_selected'])

        model = ML_Model.objects.get(pk=2)
        model.is_selected = True
        model.save()

        self.assertEqual(len(ML_Model.objects.filter(is_selected=True)), 1)
        pass

    # def test_update_모든버전(self):
    #     print(f">> test_update_모든버전")
    #     ml_model.objects.update(is_selected=False)


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class Test_Evaluate(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        test_title = 'test_model'
        test_mock = mock.MagicMock(spec=File)
        test_mock.name = 'test_model.h5'
        my_model = ML_Model.objects.create(title=test_title, model_file=test_mock)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_create_evaluation(self):
        my_model = ML_Model.objects.get(id=1)
        # my_eval = evaluation.objects.create(ml_model=my_model)
        eval_data = {
            'total': 10,
            'success': 2,
        }
        # print(eval_data)
        form = EvaluationForm(data=eval_data, instance=my_model.evaluation)  # , instance=my_eval)
        self.assertTrue(form.is_valid())
        form.save()


    def test_update_evaluation(self):
        # print(">> test_update_evaluaiton")
        my_model = ML_Model.objects.get(id=1)
        my_eval = my_model.evaluation

        # print(f"before: {my_eval.success} / {my_eval.total}")
        my_model.evaluate(1, 1)
        self.assertEqual(my_eval.success, 1)
        self.assertEqual(my_eval.total, 1)
        my_model.evaluate(1, 2)
        self.assertEqual(my_eval.success, 1)
        self.assertEqual(my_eval.total, 2)

        final_model = ML_Model.objects.get(id=1)
        final_eval = final_model.evaluation
        # print(f"before: {my_eval.success} / {my_eval.total}")
        # print(f"before: {final_eval.success} / {final_eval.total}")
        self.assertEqual(final_eval.success, my_eval.success)
        self.assertEqual(final_eval.total, my_eval.total)