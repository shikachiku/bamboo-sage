# =========================================
# Bamboo Sage 表示ユーティリティ
# =========================================

def line(length=40, char="="):
    print(char * length)


def title(text):
    line()
    print(text)
    line()


def section(text):
    print()
    line()
    print(text)
    line()


def blank():
    print()
