import { createRouter, createWebHistory } from "vue-router"

// @ts-ignore
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'

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
            path: '/',
            redirect: '/login'
        }
    ],
})

export default router