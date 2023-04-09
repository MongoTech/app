import React from 'react';
import { Tab, Row, Col, Nav } from 'react-bootstrap';
import {useSelector} from "react-redux";
import withToken from "../hocs/withToken";
const Profile = () => {
  const refEmail = React.useRef()
  const refFullName = React.useRef()
  const {email, full_name} = useSelector((store)=>store.user)

  const handleSubmit = (e) => {
    e.preventDefault()

  }
  React.useEffect(()=>{
    refEmail.current.value = email
    refFullName.current.value = full_name
  })
  return (
    <>
      <div className="settings mtb15">
        <div className="container-fluid">
          <Tab.Container defaultActiveKey="profile">
            <Row>
              <Col lg={3}>
                <Nav variant="pills" className="settings-nav">
                  <Nav.Item>
                    <Nav.Link eventKey="profile">Profile</Nav.Link>
                  </Nav.Item>
                </Nav>
              </Col>
              <Col lg={9}>
                <Tab.Content>
                  <Tab.Pane eventKey="profile">
                    <div className="card">
                      <div className="card-body">
                        <h5 className="card-title">General Information</h5>
                        <div className="settings-profile">
                          <form method="POST" onSubmit={handleSubmit}>
                            <div className="form-row mt-4">
                              <div className="col-md-6">
                                <label htmlFor="formFirst">Full name</label>
                                <input
                                  id="formFirst"
                                  type="text"
                                  className="form-control"
                                  placeholder="First name"
                                  ref={refFullName}
                                />
                              </div>

                              <div className="col-md-6">
                                <label htmlFor="emailAddress">Email</label>
                                <input
                                  id="emailAddress"
                                  type="text"
                                  className="form-control"
                                  placeholder="Enter your email"
                                  ref={refEmail}
                                />
                              </div>
                              <div className="col-md-12">
                                <input type="submit" value="Update" />
                              </div>
                            </div>
                          </form>
                        </div>
                      </div>
                    </div>
                  </Tab.Pane>
                </Tab.Content>
              </Col>
            </Row>
          </Tab.Container>
        </div>
      </div>
    </>
  );
}

export default withToken(Profile)
