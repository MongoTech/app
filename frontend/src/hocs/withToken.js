import React from "react"
import {getToken} from "../services/token";

const withProtectedRoute = (Component) =>{
    const WithToken = (props) => {
        const token = getToken()
        console.log("Token", token)
        if (!token) {
            return window.location.href = "/login"
        }
        return <Component {...props} />
    }
    return WithToken
}

export default withProtectedRoute;