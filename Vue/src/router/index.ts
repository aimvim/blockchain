import { createRouter, createWebHistory } from "vue-router"

// @ts-ignore
import Login from '@/views/Login.vue'
// @ts-ignore
import Register from '@/views/Register.vue'
// @ts-ignore
import Home from '@/views/Home.vue'
// @ts-ignore
import TaskDetail from '@/views/TaskDetail.vue'
// @ts-ignore
import CheckAccount from '@/views/CheckAccount.vue'
// @ts-ignore
import DealCommunity from '@/views/DealCommunity.vue'
// @ts-ignore
import MyBlock from '@/views/MyBlock.vue'
// @ts-ignore
import BlockDetail from '@/views/BlockDetail.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            name: 'login',
            path: '/login',
            component: Login
        },
        {
            name: 'register',
            path: '/register',
            component: Register
        },
        {
            name: 'home',
            path: '/home',
            component: Home,
        },
        {
            name: 'taskDetail',
            path: '/taskDetail',
            component: TaskDetail,
            props: true
        },
        {
            name: 'checkAccount',
            path: '/checkAccount',
            component: CheckAccount
        },
        {
            name: 'dealCommunity',
            path: '/dealCommunity',
            component: DealCommunity
        },
        {
            name: 'myBlock',
            path: '/myBlock',
            component: MyBlock
        },
        {
            name: 'blockDetail',
            path: '/blockDetail',
            component: BlockDetail
        },
        {
            path: '/',
            redirect: '/login'
        }
    ],
})

export default router