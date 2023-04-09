import React from 'react';
import {getUser, updateUser} from "../../services/api";
import {useAlert} from "react-alert";
import withToken from "../../hocs/withToken";
import {showError} from "../../utils";
import Form from '../../components/pages/users/form'
import {createAvatar} from "../../services/api";
import {useParams} from "react-router-dom";
const UsersEdit = () => {

    const refUsername = React.useRef()
    const refEmail = React.useRef()
    const refPassword = React.useRef()
    const refSuperuser = React.useRef()
    const refActive = React.useRef()
    const alert = useAlert()
    const refLabel = React.useRef()
    const [selectedFile, setSelectedFile] = React.useState([]);
    const {id} =  useParams();


    const handleOnChange = (e) => {
        setSelectedFile(e.target.files[0])
    }

    const submitHandle = (e) => {
        e.preventDefault()

        updateUser(
            id,
            refUsername.current.value,
            refEmail.current.value,
            refPassword.current.value,
            refSuperuser.current.checked,
            refActive.current.checked
        ).then((response) => {
            response.email === refEmail.current.value ? window.location.href = "/users" : showError(alert, response)
        })

        if (setSelectedFile) {
            createAvatar(selectedFile, id).then((response) => {
                console.log(response)
            }).catch((err) => alert.show("File Upload Error: " + err));
        }

    }

    React.useEffect(() => {
        getUser(id).then((user) => {
            if (id === null || user.email === null) {
                window.location.href = "/users"
            } else {
                refUsername.current.value = user.full_name
                refEmail.current.value = user.email
                refSuperuser.current.checked = user.is_superuser
                refActive.current.checked = user.is_active
            }
        })

    }, [])

    return <Form
        title={"Edit user"}
        button={"Update"}
        submitHandle={submitHandle}
        refUsername={refUsername}
        refEmail={refEmail}
        refPassword={refPassword}
        refSuperuser={refSuperuser}
        refActive={refActive}
        refLabel={refLabel}
        handleOnChange={handleOnChange}
    />
}

export default withToken(UsersEdit)