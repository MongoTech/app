import axios from "axios";
import {id2key} from "../utils";
function getAPIurl(url) {
    if ( window.location.host === "localhost:3000" ) {
        url = "http://localhost:8000/api/v1"
    }
    return url
}
const GET = (url) => {
    return axios.get(url)
    .then(function (response) {
        return response.data
    })
    .catch(function (error) {
        return error
    })
}
const POST = (url, payload) => {
    return axios.post(url, payload)
        .then(function (response) {
            return response.data
        })
        .catch(function (error) {
            return error
        })
}

const PUT = (url, payload) => {
    return axios.put(url, payload)
        .then(function (response) {
            return response.data
        })
        .catch(function (error) {
            return error
        })
}
const DELETE = (url) => {
    return axios.delete(url)
        .then(function (response) {
            return response.data
        })
        .catch(function (error) {
            return error
        })
}
const auth = (authenticate) => {
    return axios({
            method: 'post',
            url: getAPIurl("/api") + '/login/access-token',
            data: authenticate,
            withCredentials: true,
            headers: {"Content-Type": "multipart/form-data"}
        }
        , authenticate)
        .then(function (response) {
            return response
        })
        .catch(function (error) {
            return error
        });
}
const register = (name, email, password) => {
    return POST(getAPIurl("/api") + '/users/open', {
        "email": email,
        "full_name": name,
        "password": password
    })
}
const recovery = (email) => {
    return POST(getAPIurl("/api") + '/password-recovery/' + email)
}
const reset = (token, password) => {
    return POST(getAPIurl("/api") + '/reset-password/', {
        "token": token,
        "new_password": password
    })
}
const getUserMe = () => {
    return GET(getAPIurl("/api") + '/users/me')
}
const createAvatar = (file, user_id = null) => {
    const formData = new FormData();
    formData.append("file", file);
    return POST("/api/users/avatar/?user_id=" + user_id , formData);
}

const getStats = () => {
    return GET(getAPIurl("/api") + '/users/stats')
}


const getPagination = (url) => {
    return GET(getAPIurl("/api") + '/' + url + '/pagination')
}

// USERS
const createUser = (full_name, email, password, is_superuser, is_active) => {
    return POST(getAPIurl("/api") + '/users/', {
        "email": email,
        "is_active": is_active,
        "is_superuser": is_superuser,
        "full_name": full_name,
        "avatar": "string",
        "description": "string",
        "password": password
    })
}
const getUsers = (skip=0, limit=10) => {
    return id2key(GET(getAPIurl("/api") + '/users/?skip=' + skip + '&limit=' + limit))
}
const getUser = (id) => {
    return GET(getAPIurl("/api") + '/users/' + id)
}
const updateUser = (id, full_name, email, password, is_superuser, is_active) => {
    return PUT(getAPIurl("/api") + '/users/' + id, {
        "email": email,
        "is_active": is_active,
        "is_superuser": is_superuser,
        "full_name": full_name,
        "avatar": "string",
        "description": "string",
        "password": password
    })
}
const deleteUser = (id) => {
    return DELETE(getAPIurl("/api") + '/users/' + id)
}

export {
    auth, register, recovery, reset,
    getUserMe, createUser, getUsers, getUser, updateUser, deleteUser, createAvatar, getStats,
    getPagination,
    GET, getAPIurl
}
