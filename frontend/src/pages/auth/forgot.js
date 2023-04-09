import Forgot from "../../components/pages/auth/forgot";
import React from "react"
import {useHistory} from "react-router-dom";
import {useAlert} from "react-alert";
import {recovery} from "../../services/api";
export default function ForgotPage() {
    const refEmail = React.useRef()
    const history = useHistory()
    const alert = useAlert()
    const submitHandler = async (e) => {
        e.preventDefault()
        const response = await recovery(refEmail.current.value)

        if (response.msg) {
            history.push("/check")
        } else {
            alert.show(response.response.data.detail)
        }


    }
    React.useEffect(() => {
        refEmail.current.focus()
    })
    return <Forgot refEmail={refEmail} submitHandler={submitHandler} />
}