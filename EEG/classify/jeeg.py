import subprocess, os

def train(model_name, task_file, eeg_file):
    cur_path = os.path.dirname(os.path.realpath(__file__))
    train_jar = os.path.join(cur_path, 'jeeg/train.jar')

    models_folder = os.path.join(cur_path, 'models')
    model_path = os.path.join(models_folder, model_name)
    args = [model_path]

    output, _ = subprocess.Popen(['java', '-jar', train_jar] + args,
                     stdout=subprocess.PIPE).communicate()
    success = True if output == 'success' else False
    return model_path

def apply(model_name, task_file, eeg_file):
    cur_path = os.path.dirname(os.path.realpath(__file__))
    test_jar = os.path.join(cur_path, 'jeeg/test.jar')

    models_folder = os.path.join(cur_path, 'models')
    model_path = os.path.join(models_folder, model_name)
    args = [model_path]

    output, _ = subprocess.Popen(['java', '-jar', test_jar] + args,
                     stdout=subprocess.PIPE).communicate()
    success = True if output == 'success' else False
    return task_file
