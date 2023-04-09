import Login from '../../components/pages/auth/login'
import {auth} from "../../services/api";
import React from "react";
import {useAlert} from "react-alert";
import {getToken} from "../../services/token";
import {showError} from "../../utils";
import {useHistory} from "react-router-dom";

export default function LoginPage() {
    const refUsername = React.useRef()
    const refPassword = React.useRef()
    const alert = useAlert()
    const history = useHistory()
    if (getToken()) {
        history.push("/dashboard")
    }
    const submitHandler = async (e) => {
        e.preventDefault()

        const authenticate = {
            'username': refUsername.current.value,
            'password': refPassword.current.value
        }

        auth(authenticate).then((response) => {
            if (response && response.code !== "ERR_NETWORK") {
                window.location.pathname = '/inactive'
            } else {
                showError(alert, response ? response : "Login error")
            }
        })

        return false
    }

    React.useEffect(() => {
        refUsername.current.focus()
    }, [])
    return <Login
        refUsername={refUsername}
        refPassword={refPassword}
        submitHandler={submitHandler}
    />
}