# -*- coding:GB2312 -*-
# %%
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('hfl/rbt3')

tokenizer.batch_encode_plus(
['һ����Ϫһ��ɽ', '�����Ծ���Ƽ�'],
truncation=True,
)

# %%
#��6��/�Ӵ��̼������ݼ�
from datasets import load_from_disk, Dataset
# dataset = load_from_disk('./data/ChnSentiCorp/')
# print(type(dataset), dataset[0:50])

dataset_train = Dataset.from_file('./data/chn_senti_corp/chn_senti_corp-train.arrow')
dataset_test = Dataset.from_file('./data/chn_senti_corp/chn_senti_corp-test.arrow')
dataset_valid = Dataset.from_file('./data/chn_senti_corp/chn_senti_corp-validation.arrow')
print(type(dataset_train), dataset_train[0:50])

# %%
# ��С���ݹ�ģ�����ڲ���
dataset_train= dataset_train.shuffle().select(range(3000))
dataset_test= dataset_test.shuffle().select(range(200))
print(type(dataset_train))

# %%
#��6��/����
def f(data):
    return tokenizer.batch_encode_plus(data['text'],truncation=True)

dataset_train=dataset_train.map(f,
batched=True,
batch_size=100,
# num_proc=4,
remove_columns=['text'])

print(dataset_train)
# %%
print(dataset_test)
dataset_test=dataset_test.map(f,
batched=True,
batch_size=100,
# num_proc=4,
remove_columns=['text'])

# %%
print(type(dataset_test), len(dataset_test), dataset_test)
# %%
def filter_func(data):
    return [len(i)<=512 for i in data['input_ids']]

dataset_train=dataset_train.filter(filter_func, batched=True, batch_size=100)

dataset_test=dataset_test.filter(filter_func, batched=True, batch_size=100)

print(type(dataset_train), len(dataset_train), dataset_train)
print(type(dataset_test), len(dataset_test), dataset_test)

# %%
from transformers import AutoModelForSequenceClassification
import torch
model=AutoModelForSequenceClassification.from_pretrained('hfl/rbt3',num_labels=2)
# #ͳ��ģ�Ͳ�����
# sum([i.nelement() for i in model.parameters()]) / 10000
# # %%
# #��6��/ģ������
# #ģ��һ������
# data = {
# 'input_ids': torch.ones(40, 100, dtype=torch.long),
# 'token_type_ids': torch.ones(40, 100, dtype=torch.long),
# 'attention_mask': torch.ones(40, 100, dtype=torch.long),
# 'labels': torch.ones(40, dtype=torch.long)
# }#ģ������

# out = model(**data)
# out['loss'], out['logits'].shape
# %%
#��6��/��������ָ��
from datasets import load_metric
metric = load_metric('accuracy')

#��6��/�������ۺ���
import numpy as np
from transformers.trainer_utils import EvalPrediction
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    logits = logits.argmax(axis=1)
    return metric.compute(predictions=logits, references=labels)

#ģ�����
eval_pred = EvalPrediction(
predictions=np.array([[0, 1], [2, 3], [4, 5], [6, 7]]),
label_ids=np.array([1, 1, 0, 1]),
)
# %%
print("1 >> ", compute_metrics(eval_pred))
print(eval_pred.predictions.shape, eval_pred.label_ids.shape)
# %%
#��6��/����ѵ������
from transformers import TrainingArguments
#����ѵ������
args = TrainingArguments(
#������ʱ���ݱ���·��
output_dir='./output_dir/third/',
#�������ִ�еĲ��ԣ���ȡֵΪno��epoch��steps
evaluation_strategy='steps',
#����ÿ�����ٸ�stepִ��һ�β���
eval_steps=30,
#����ģ�ͱ�����ԣ���ȡֵΪno��epoch��steps
save_strategy='steps',
#����ÿ�����ٸ�step����һ��
save_steps=30,
#���干ѵ�������ִ�
num_train_epochs=2,
learning_rate=1e-4,#����ѧϰ��
#�������Ȩ��˥������ֹ�����
weight_decay=1e-2,
#������Ժ�ѵ��ʱ�����δ�С
per_device_eval_batch_size=16,
per_device_train_batch_size=16,
#�����Ƿ�Ҫʹ��GPUѵ��
no_cuda=False,
)
# %%
#��6��/����ѵ����
from transformers import Trainer
from transformers.data.data_collator import DataCollatorWithPadding
#����ѵ����
trainer = Trainer(
model=model,
args=args,
train_dataset=dataset_train,
eval_dataset=dataset_test,
compute_metrics=compute_metrics,
data_collator=DataCollatorWithPadding(tokenizer),
)

# %%
#��6��/��������������
data_collator = DataCollatorWithPadding(tokenizer)
#��ȡһ������
data = dataset_train[:5]
#�����Щ���ӵĳ���
for i in data['input_ids']:
    print(len(i))
#��������������
data = data_collator(data)
#�鿴����������
for k, v in data.items():
    print(k, v.shape)
# %%
tokenizer.decode(data['input_ids'][0])
# %%
#����ģ��
trainer.evaluate()

# %%
#��6��/ѵ��
trainer.train()
# %%
trainer.evaluate()


# %%
trainer.save_model(output_dir='./output_dir/save_model_third')
# %%
# import torch
# print(torch.cuda.is_available())
# device = torch.device("cuda:0")
# print(device)
# %%
# trainer.train(resume_from_checkpoint='./output_dir/checkpoint-90')

# %%
