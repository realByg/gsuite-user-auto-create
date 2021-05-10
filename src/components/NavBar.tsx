import React from 'react'
import {Row, Col, Space} from 'antd'
import CustomIcon from '../utils/custom-icon'

export default function NavBar() {
    const gsFont = {
        fontWeight: 500,
        fontSize: 24
    }

    return (
        <Row style={{height: '100%'}}>
            <Col lg={{span: 18, offset: 3}}
                 xs={{span: 22, offset: 1}}
            >
                <div className='display-flex align-center justify-between'>
                    <Space align='center'>
                        <img
                            style={{height: 28}}
                            src='https://i.loli.net/2020/05/31/GK2zyeg9XRlZIw7.png'
                            alt='google'
                        />

                        <div
                            className='hide-on-small'
                            style={gsFont}
                        >
                            |
                        </div>

                        <div
                            style={gsFont}
                            className='hide-on-small'
                        >
                            Google Workspace
                        </div>
                    </Space>

                    <Space align='center'>
                        <CustomIcon
                            style={{
                                fontSize: 30
                            }}
                            type='iconGoogle1'
                            className='hide-on-small'
                        />

                        <CustomIcon
                            style={{
                                fontSize: 30
                            }}
                            type='icon-businessclouddatadatabasedrivestora'
                        />

                        <CustomIcon
                            style={{
                                fontSize: 30
                            }}
                            type='icongoogle-photos--'
                        />

                        <CustomIcon
                            style={{
                                fontSize: 30
                            }}
                            type='iconicons-google-cloud-platform'
                        />

                        <CustomIcon
                            style={{
                                fontSize: 30
                            }}
                            type='iconGmail'
                            className='hide-on-small'
                        />

                        <CustomIcon
                            style={{
                                fontSize: 30
                            }}
                            type='icongoogle-plus'
                            className='hide-on-small'
                        />
                    </Space>
                </div>
            </Col>
        </Row>
    )
}
