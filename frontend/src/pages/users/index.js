import React from 'react';
import {getUsers, deleteUser, getPagination} from "../../services/api";
import {useAlert} from "react-alert";
import withToken from "../../hocs/withToken";
import List from "../../components/pages/users/list"
import {deleteRow, showError} from "../../utils";

const UsersList = () => {
    const [users, setUsers] = React.useState([]);
    const [pages, setPages] = React.useState(0)
    const [page, setPage] = React.useState(1)
    const alert = useAlert()
    console.log("Users list")
    const editHandler = (id) => {
        window.location.href = "/users/edit/" + id
    }
    const deleteHandler = (id) => {
        deleteRow(id)
        setTimeout(() => {
            deleteUser(id).then((response) => {
                response.email ? document.getElementById("tr" + id).remove() : showError(alert, response)
            })
        }, 500)


    }
    React.useEffect(() => {
        getPagination('users')
            .then(setPages)
            .catch(error => alert.show(error));
    }, [alert])
    React.useEffect(() => {
        const current_page = window.location.pathname.split("/")[2]
        setPage(current_page ? parseInt(current_page):1)
        getUsers((page - 1) * 10, 10)
            .then(setUsers)
            .catch(error => alert.show(error));

    }, [page])
    return (<List
        users={users}
        editHandler={editHandler}
        deleteHandler={deleteHandler}
        pages={pages}
        setPage={setPage}
    />);
}

export default withToken(UsersList)