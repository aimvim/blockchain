**Login**的API
UserLogin   VolunteerLogin      AdmninLogin
传入的Json文档为
```json
{"id":"id",
"password":"password"
```
返回的都是表示成功的信息，没啥作用，直接看状态码吧(成功是200，失败是400，下面的也是一样)

**Register**的API
volunteer_register
```json
{
  "id": "id",
  "password": "pass"
}
```
admin_register
```json
{
    "id":id,
    "passwd":passwd,
    "invite_code":inco,
    "register_code":rco
    }
```
user_register
```json
{
    "id":id,
    "passwd":pwd,
    "register_code":rco,
    "proof":url
    }
```