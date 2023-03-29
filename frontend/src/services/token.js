const saveToken = async (token) => {
    if (token) {
        localStorage.setItem('access-token', token)
    }
}
const getToken = () => {
    return  document.cookie.split("token=")[1]
}
const deleteToken = () => {
    document.cookie = 'token=; Max-Age=-99999999;';
    window.location.href = "/login"
}
export {saveToken, getToken, deleteToken}