import React from 'react';
import {createUser} from "../../services/api";
import {useAlert} from "react-alert";
import withToken from "../../hocs/withToken";
import Form from '../../components/pages/users/form'
import {showError} from "../../utils";

const UsersNew = () => {
    const refUsername = React.useRef()
    const refEmail = React.useRef()
    const refPassword = React.useRef()
    const refSuperuser = React.useRef()
    const refActive = React.useRef()
    const alert = useAlert()
    const submitHandle = (e) => {
        e.preventDefault()

        createUser(refPassword.current.value,
            refEmail.current.value,
            refPassword.current.value,
            refSuperuser.current.checked,
            refActive.current.checked
        )
        .then((response) => {
            response.email === refEmail.current.value ? window.location.href = "/users" : showError(alert, response)
        })
    }
    return (<Form
        title={"Add new user"}
        button={"Add"}
        submitHandle={submitHandle}
        refUsername={refUsername}
        refEmail={refEmail}
        refPassword={refPassword}
        refSuperuser={refSuperuser}
        refActive={refActive}
    />)
}

export default withToken(UsersNew)