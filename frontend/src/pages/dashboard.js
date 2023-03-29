import withToken from "../hocs/withToken";
import {getStats} from "../services/api";
import React from "react"
import {Table} from 'react-bootstrap';
const Dashboard = () => {
    const [stats, setStats] = React.useState({})

    React.useEffect(()=>{
        getStats().then(setStats)
    },[])
    return <>        <>
            <h1>Global stats</h1>
            <Table striped bordered hover style={{width: "400px", margin: "20px"}}>
                <thead>
                <tr>
                    <th style={{backgroundColor: "#cccccc", color: "#000000"}}>Metric</th>
                    <th style={{backgroundColor: "#cccccc", color: "#000000"}}>Value</th>
                </tr>
                </thead>
                <tbody>

                <tr>
                    <td>Total users</td>
                    <td><a href="/users">{stats.users}</a></td>
                </tr>

                </tbody>
            </Table>
        </></>
}

export default withToken(Dashboard)