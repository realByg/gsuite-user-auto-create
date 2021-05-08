import React, {useState} from 'react'
import {Row, Col, Button, Space, Modal} from 'antd'

import ContentForm from './ContentForm'


export default function Content() {
    const contentBg = {
        background: 'url(https://i.loli.net/2020/01/22/Rgv3xJAVYN4n9Za.png) no-repeat',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        height: '100vh'
    }

    const [modalVisible, setModalVisible] = useState(false)

    return (
        <Row style={contentBg}>
            <Col lg={{span: 14, offset: 5}}
                 xs={{span: 22, offset: 1}}
                 className='display-flex align-center justify-around'
            >
                <div className='text-center'>
                    <span className='lineOneFont'>
                        Google Workspace / G Suite
                    </span>

                    <br/>

                    <span className='lineTwoFont'>
                        Everything you need to get anything done.
                    </span>

                    <br/>
                    <br/>

                    <Space>
                        <Button
                            style={{width: 110}}
                            type='primary'
                            danger
                            size='large'
                            onClick={() => setModalVisible(v => !v)}
                        >
                            立即获取
                        </Button>

                        <Modal
                            title='获取 G Suite for Education'
                            centered
                            visible={modalVisible}
                            width={1000}
                            maskClosable={false}
                            destroyOnClose
                            footer={false}
                            onCancel={() => setModalVisible(false)}
                        >
                            <ContentForm/>
                        </Modal>

                        <Button
                            style={{width: 110}}
                            size='large'
                            onClick={() =>
                                window.open('https://accounts.google.com/ServiceLogin')
                            }
                        >
                            登录
                        </Button>
                    </Space>
                </div>
            </Col>
        </Row>
    )
}
