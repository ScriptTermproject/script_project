#include "python.h" 

static PyObject*

spam_strlen(PyObject* self, PyObject* args)
{
    const char* str = NULL;
    int len;

    if (!PyArg_ParseTuple(args, "s", &str)) // 매개변수 값을 분석하고 지역변수에 할당 시킵니다.
        return NULL;

    len = strlen(str);

    return Py_BuildValue("i", len);
}

static PyObject*
spam_temp(PyObject* self, PyObject* args)
{
    float tm = 0;
    float tp, ws = 0;

    if (!PyArg_ParseTuple(args, "ff", &tp, &ws)) //피제수와 제수 할당
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
    "체감 기온 계산"},
    {NULL, NULL, 0, NULL}    //배열의 끝을 나타낸다.
};


static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",            // 모듈 이름
    "It is test module.", // 모듈 설명을 적는 부분, 모듈의 __doc__에 저장됩니다.
    -1,SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    return PyModule_Create(&spammodule);
}
