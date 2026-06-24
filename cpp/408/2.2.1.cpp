#include <iostream>
using namespace std;

#define MaxSize 100

typedef int ElemType;

typedef struct {
    ElemType data[MaxSize];
    int length;
} SqList;

bool Del_Min(SqList &L, ElemType &value) {
    if (L.length == 0) {
        cout << "顺序表为空，删除失败！" << endl;
        return false;
    }

    value = L.data[0];
    int minPos = 0;

    for (int i = 1; i < L.length; i++) {
        if (L.data[i] < value) {
            value = L.data[i];
            minPos = i;
        }
    }

    L.data[minPos] = L.data[L.length - 1];

    L.length--;

    return true;
}

void PrintList(SqList L) {
    for (int i = 0; i < L.length; i++) {
        cout << L.data[i] << " ";
    }
    cout << endl;
}

int main() {
    SqList L;

    L.length = 5;
    L.data[0] = 10;
    L.data[1] = 3;
    L.data[2] = 8;
    L.data[3] = 20;
    L.data[4] = 6;

    cout << "删除前顺序表为：";
    PrintList(L);

    ElemType deletedValue;

    if (Del_Min(L, deletedValue)) {
        cout << "被删除的最小值是：" << deletedValue << endl;
        cout << "删除后顺序表为：";
        PrintList(L);
    }

    return 0;
}