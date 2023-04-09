import Reset from '../../components/pages/auth/reset'
import {useAlert} from "react-alert";
import {showError} from "../../utils";
import {reset, auth} from "../../services/api"
import React from "react"
import {saveToken} from "../../services/token";
import {useHistory} from "react-router-dom";
export default function ResetPage() {
    const refPassword = React.useRef()
    const refPassword2 = React.useRef()
    const history = useHistory()
    const alert = useAlert()

    const submitHandler = (e) => {
        e.preventDefault()
        const password = refPassword.current.value
        const password2 = refPassword2.current.value
        if (password !== password2) {
            showError(alert, "Password mismatch")
        } else {
            const token = window.location.search.split("?token=")[1]
            reset(token, password).then((response) => {
                if  (response.id) {
                    const email = response.email
                    auth({"username": email, "password": password}).then((response) => {
                        if (response.status === 200) {
                            saveToken(response.data.access_token).then()
                            history.push("/dashboard")
                        } else {
                            showError(alert, response)
                        }
                    })
                } else {
                    showError(alert, response)
                }


            })
        }


    }
    return <Reset
        refPassword={refPassword}
        refPassword2={refPassword2}
        submitHandler={submitHandler}
    />
}