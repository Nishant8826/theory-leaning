import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";


export const api = createApi({
    baseQuery: fetchBaseQuery({ baseUrl: "http://localhost:3000" }),
    tagTypes: ['Task'],
    endpoints: (builder) => ({
        getTasks: builder.query({
            query: () => "/tasks",
            transformResponse: (task) => task.reverse(),
            providesTags: ['Task'],
        }),
        addTasks: builder.mutation({
            query: (task) => ({
                url: "/tasks",
                method: "POST",
                body: task
            }),
            invalidatesTags: ['Task'],
            async onQueryStarted(task, { dispatch, queryFulfilled }) {
                const patchResult = dispatch(api.util.updateQueryData("getTasks", undefined, (draftTaskList) => {
                    draftTaskList.unshift({ id: crypto.randomUUID(), ...task });
                }));

                try {
                    await queryFulfilled;
                } catch (error) {
                    patchResult.undo();
                };
            }
        }),
        updateTask: builder.mutation({
            query: ({ id, ...updatedTask }) => ({
                url: `/tasks/${id}`,
                method: 'PATCH',
                body: updatedTask
            }),
            invalidatesTags: ['Task'],
            async onQueryStarted(task, { dispatch, queryFulfilled },) {
                const patchResult = dispatch(api.util.updateQueryData("getTasks", undefined, (draftedTasksList) => {
                    const taskIndex = draftedTasksList.findIndex((el) => el.id === task.id);
                    draftedTasksList[taskIndex] = { ...draftedTasksList[taskIndex], ...task };
                }));

                try {
                    await queryFulfilled;
                } catch {
                    patchResult.undo();
                }
            },
        }),
        deleteTask: builder.mutation({
            query: (id) => ({
                url: `/tasks/${id}`,
                method: 'DELETE',
            }),
            invalidatesTags: ['Task'],
            async onQueryStarted(id, { dispatch, queryFulfilled },) {
                const patchResult = dispatch(api.util.updateQueryData("getTasks", undefined, (draftedTasksList) => {
                    const taskIndex = draftedTasksList.findIndex((el) => el.id === id);
                    draftedTasksList.splice(taskIndex, 1)
                }));

                try {
                    await queryFulfilled;
                } catch {
                    patchResult.undo();
                }
            },
        }),
    })
})


export const { useGetTasksQuery, useAddTasksMutation, useUpdateTaskMutation, useDeleteTaskMutation } = api;