#include "python.h" 

static PyObject*

spam_strlen(PyObject* self, PyObject* args)
{
    const char* str = NULL;
    int len;

    if (!PyArg_ParseTuple(args, "s", &str)) // �Ű����� ���� �м��ϰ� ���������� �Ҵ� ��ŵ�ϴ�.
        return NULL;

    len = strlen(str);

    return Py_BuildValue("i", len);
}

static PyObject*
spam_temp(PyObject* self, PyObject* args)
{
    float tm = 0;
    float tp, ws = 0;

    if (!PyArg_ParseTuple(args, "ff", &tp, &ws)) //�������� ���� �Ҵ�
        return NULL;
    float V = pow((ws * 3.6), (0.16));
    float T = tp;
    tm = 13.12 + 0.6215 * T - 11.37 * V + 0.3965 * V * T;


    return Py_BuildValue("f", tm);
}


static PyMethodDef SpamMethods[] = {
    {"strlen", spam_strlen, METH_VARARGS,
    "count a string length."},
    {"temp", spam_temp, METH_VARARGS,
    "ü�� ��� ���"},
    {NULL, NULL, 0, NULL}    //�迭�� ���� ��Ÿ����.
};


static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",            // ��� �̸�
    "It is test module.", // ��� ������ ���� �κ�, ����� __doc__�� ����˴ϴ�.
    -1,SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}
