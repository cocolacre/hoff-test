Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# must be started NOT as administrator.