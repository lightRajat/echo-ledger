import { createRouter, createWebHistory } from 'vue-router';

import Skeleton from '@/components/Skeleton.vue';
import Home from '@/views/Home.vue';
import Recorder from '@/views/Recorder.vue';
import Dashboard from '@/views/Dashboard.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/', name: 'skeleton', component: Skeleton, children: [
                { path: '/', name: 'home', component: Home },
                { path: '/recorder', name: 'recorder', component: Recorder },
                { path: '/dashboard', name: 'dashboard', component: Dashboard },
            ]
        }
    ]
});

router.afterEach((to) => {
    document.title = to.meta.title || "Echo Ledger";
});

export default router;