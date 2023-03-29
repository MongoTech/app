import Signup from '../../components/pages/auth/signup'
import {useAlert} from "react-alert";
import {showError} from "../../utils";
import {register, auth} from "../../services/api"
import React from "react"
import {getToken} from "../../services/token";
import {useHistory} from "react-router-dom";
export default function SignUpPage() {
    const refName = React.useRef()
    const refEmail = React.useRef()
    const refPassword = React.useRef()
    const refPassword2 = React.useRef()
    const history = useHistory()
    const alert = useAlert()
    if (getToken()) {
        history.push("/dashboard")
    }
    const submitHandler = (e) => {
        e.preventDefault()

        const full_name = refName.current.value
        const email = refEmail.current.value
        const password = refPassword.current.value
        const password2 = refPassword2.current.value
        if (password !== password2) {
            showError(alert, "Password mismatch")
        } else {
            register(full_name, email, password).then((response) => {
                if  (response.id) {
                    auth({"username": email, "password": password}).then((response) => {
                        if (response) {
                            window.location.href = "/inactive"
                        } else {
                            alert.show(response.response.data.detail)
                        }
                    })
                } else {
                    showError(alert, response)
                }


            })
        }


    }
    return <Signup
        refName={refName}
        refEmail={refEmail}
        refPassword={refPassword}
        refPassword2={refPassword2}
        submitHandler={submitHandler}
    />
}