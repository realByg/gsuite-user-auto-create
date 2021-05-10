import React, {useState, useEffect} from 'react'
import {Spin, Form, Button, Input, message, Row, Col, Select} from 'antd'
import {CopyOutlined, KeyOutlined, MailOutlined} from '@ant-design/icons'
import copy from 'copy-to-clipboard'
import axios from 'axios'


export default function ContentForm() {
    const [spinning, setSpinning] = useState(false)
    const [gsConfig, setGsConfig] = useState([
        {
            domains: [],
            id: '0',
            name: '',
        },
    ])
    const [domains, setDomains] = useState([])
    const [createdAccount, setCreatedAccount] = useState({
        email: '',
        password: '',
    })
    const [form] = Form.useForm()

    const createUser = (formData: object) => {
        setSpinning(true)
        axios({
            method: 'post',
            url: 'createUser',
            baseURL: process.env.REACT_APP_API_BASE_URL,
            data: formData,
        })
            .then(async (r: any) => {
                if (r.data.success) {
                    message.success('账号创建成功')
                    setCreatedAccount({
                        email: r.data.account.primaryEmail,
                        password: r.data.account.password,
                    })
                } else {
                    message.error(r.data.msg)
                    form.resetFields()
                }
            })
            .catch(async (e: any) => {
                message.error(e)
            })
            .then(() => {
                setSpinning(false)
            })
    }

    useEffect(() => {
        setSpinning(true)
        axios({
            method: 'post',
            url: 'getGSConfig',
            baseURL: process.env.REACT_APP_API_BASE_URL,
        })
            .then((r: any) => {
                setGsConfig(r.data)
            })
            .catch(async (e: any) => {
                message.error(e)
            })
            .then(() => {
                setSpinning(false)
            })
    }, [])

    useEffect(() => {
        form.setFieldsValue({
            'email': {
                'domain': domains[0]
            }
        })
    }, [domains, form])

    const CreatedForm = (
        <Form
            labelCol={{span: 4}}
            wrapperCol={{span: 20}}
        >
            <Form.Item label="邮箱">
                <Input
                    value={createdAccount.email}
                    prefix={<MailOutlined/>}
                    suffix={<CopyOutlined
                        onClick={async () => {
                            copy(createdAccount.email)
                            message.success('已复制邮箱')
                        }}
                    />}
                />
            </Form.Item>

            <Form.Item label="密码">
                <Input
                    value={createdAccount.password}
                    prefix={<KeyOutlined/>}
                    suffix={<CopyOutlined
                        onClick={async () => {
                            copy(createdAccount.password)
                            message.success('已复制密码')
                        }}
                    />}
                />
            </Form.Item>

            <Form.Item style={{float: 'right'}}>
                <Button
                    onClick={() =>
                        window.open('https://accounts.google.com/ServiceLogin')}
                    type="primary"
                    htmlType="submit"
                >
                    登录
                </Button>
            </Form.Item>
        </Form>
    )

    const CreateForm = (
        <Form
            form={form}
            name="basic"
            onFinish={createUser}
            labelCol={{span: 4}}
            wrapperCol={{span: 20}}
        >
            <Form.Item
                label="机构"
                name="institute"
                rules={[{required: true, message: '必选'}]}
            >
                <Select
                    placeholder="选择机构"
                    onChange={v => {
                        const selectedGs = gsConfig.find(gs => gs.id === v)
                        setDomains(
                            selectedGs?.domains || []
                        )
                    }}
                >
                    {gsConfig.map(gs => (
                        <Select.Option
                            value={gs.id}
                            key={gs.id}
                        >
                            {gs.name}
                        </Select.Option>
                    ))}
                </Select>
            </Form.Item>

            <Form.Item
                label="邮箱"
                name="email"
                rules={[{
                    required: true,
                    message: '必填',
                }]}
            >
                <Input.Group compact>
                    <Form.Item
                        name={['email', 'username']}
                        noStyle
                        rules={[{
                            required: true,
                            message: '必填，1-10个字符，仅限字母数字',
                            min: 1,
                            max: 10,
                            type: 'string',
                            pattern: /^[a-zA-Z0-9._]+$/g
                        }]}
                    >
                        <Input
                            style={{width: '55%'}}
                            placeholder="用户名"
                            allowClear
                        />
                    </Form.Item>

                    <Form.Item
                        name={['email', 'domain']}
                        noStyle
                        rules={[{required: true, message: '必选'}]}
                    >
                        <Select
                            style={{width: '45%'}}
                            placeholder="选择后缀"
                            value={domains[0]}
                            notFoundContent="请选择机构"
                        >
                            {domains.map(d => (
                                <Select.Option
                                    value={d}
                                    key={d}
                                >
                                    @{d}
                                </Select.Option>
                            ))}
                        </Select>
                    </Form.Item>
                </Input.Group>
            </Form.Item>

            <Form.Item
                label="激活码"
                name="code"
                rules={[{
                    required: true,
                    message: '格式错误',
                    type: 'string',
                    pattern: /^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$/i
                }]}
            >
                <Input
                    placeholder="激活码"
                    allowClear
                    // addonAfter={(
                    //     <a href={officeConfig.getCodeLink}
                    //        target='_blank' rel='noreferrer'
                    //     >获取激活码</a>
                    // )}
                />
            </Form.Item>

            <Form.Item style={{float: 'right'}}>
                <Button
                    type="primary"
                    htmlType="submit"
                >
                    提交
                </Button>
            </Form.Item>
        </Form>
    )


    return (
        <Spin spinning={spinning}>
            <Row>
                <Col
                    lg={{span: 14, offset: 5}}
                    xs={{span: 24}}
                >
                    {!!createdAccount.password ? CreatedForm : CreateForm}
                </Col>
            </Row>
        </Spin>
    )
}
