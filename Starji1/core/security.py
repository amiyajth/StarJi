from passlib.context import CryptContext

# 密码加密上下文（使用 bcrypt 算法）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    将明文密码转换为哈希密码
    - 同一个密码每次加密结果都不一样（加了盐）
    - 但验证时能正确匹配
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确
    - plain_password: 用户输入的明文密码
    - hashed_password: 数据库里存的哈希密码
    """
    return pwd_context.verify(plain_password, hashed_password)
