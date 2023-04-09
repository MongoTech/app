import Pagination from 'react-bootstrap/Pagination';
import {useHistory} from "react-router-dom";

export default function Pages({pages, setPage}) {
    const history = useHistory()
    const current_page = window.location.pathname.split("/")[2]
    let active = current_page? parseInt(current_page) : 1;
    let items = [];
    const url = "/" + window.location.pathname.split("/")[1] + "/"
    const paginationClicked = (id) => {
        history.push(url + id)
        setPage(id)
    }
    for (let number = 1; number <= pages; number++) {
        items.push(
            <Pagination.Item key={number} active={number === active} onClick={(event) => paginationClicked(number)}>
                {number}
            </Pagination.Item>,
        );
    }


    return (<>
        <Pagination>{items}</Pagination>
    </>);
}