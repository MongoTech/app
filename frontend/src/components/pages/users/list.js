import CheckIcon from "@mui/icons-material/Check";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import React from "react";
import Pagination from '../../Pagination'
import {useHistory} from "react-router-dom";
export default function List({users, editHandler, deleteHandler, pages, setPage}) {
    const history = useHistory()
    const u = Object.values(users)

    return (<>
        <h3>List of users  <button className="btn btn-primary" onClick={()=>{history.push("/users/new")}}>Add user</button></h3>
        <table className="table star-active">
            <thead>
            <tr>
                <th width="5%">ID</th>
                <th width="20%">Full name</th>
                <th width="20%">Email</th>
                <th width="10%">Is superuser</th>
                <th width="10%">Is active</th>
                <th width="10%"></th>
            </tr>
            </thead>
            <tbody>

            {u.map((user) => {
                const {id, full_name, email, is_superuser, is_active} = user;
                return (
                    <tr key={id} id={"tr" + id}>
                        <td className={"td" + id}>{id}</td>
                        <td className={"td" + id}>{full_name}</td>
                        <td className={"td" + id}>{email}</td>
                        <td className={"td" + id}>{is_superuser ? <CheckIcon/> : ''}</td>
                        <td className={"td" + id}>{is_active ? <CheckIcon/> : ''}</td>
                        <td className={"td" + id}><EditIcon onClick={() => editHandler(id)}/></td>
                        <td className={"td" + id}><DeleteIcon onClick={() => deleteHandler(id)}/></td>
                    </tr>
                );
            })}


            </tbody>
        </table>
        <Pagination
        pages={pages}
        setPage={setPage}
        />
    </>)
}