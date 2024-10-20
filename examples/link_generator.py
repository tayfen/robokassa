from robokassa import Robokassa, HashAlgorithm

robokassa = Robokassa(
    merchant_login="my_login",
    password1="password",
    password2="password",
    is_test=False,
    algorithm=HashAlgorithm.md5
)

my_link = robokassa.payment.link.generate_by_script(
    out_sum=1000,
    inv_id=0
)
