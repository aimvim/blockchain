import { createRouter, createWebHistory } from "vue-router"

// @ts-ignore
import Login from '@/views/Login.vue'
import Register from '@/views/Register.vue'
import Home from '@/views/Home.vue'

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
            component: Home
        },
        {
            path: '/',
            redirect: '/login'
        }
    ],
})

export default router