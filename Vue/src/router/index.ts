import { createRouter, createWebHistory } from "vue-router"

// @ts-ignore
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Home from '@/views/Home.vue'
import TaskDetail from '@/views/TaskDetail.vue'
import CheckAccount from '@/views/CheckAccount.vue'

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
            path: '/',
            redirect: '/login'
        }
    ],
})

export default router