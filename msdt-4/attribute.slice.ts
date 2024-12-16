import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import $api from '../../http'
import { Statuses } from '../../assets/enums/enums'

const initialState: {
	attribute: string[]
	status: Statuses
} = {
	attribute: [],
	status: Statuses.LOADING,
}

type AttributeResponse = {
	id: number
	name: string
	slug: string
	url: string
}[]
export const fetchAttribute = createAsyncThunk(
	'attribute/FetchAttributes',
	async (params: { path: string }) => {
		const { path } = params
		const res = await $api.get<AttributeResponse>(path)
		const array = res.data.map(val => {
			return val.name
		})
		return array
	}
)
const attributeSlice = createSlice({
	name: 'attribute',
	initialState,
	reducers: {
		setAttribute(state, action: PayloadAction<string[]>) {
			state.attribute = action.payload
		},
	},
	extraReducers: builder => {
		builder.addCase(fetchAttribute.fulfilled, (state, action) => {
			state.attribute = action.payload
			state.status = Statuses.SUCCESS
		})
		builder.addCase(fetchAttribute.pending, state => {
			state.attribute = []
			state.status = Statuses.LOADING
		})
		builder.addCase(fetchAttribute.rejected, state => {
			state.attribute = []
			state.status = Statuses.ERROR
		})
	},
})
export const { setAttribute } = attributeSlice.actions
export default attributeSlice.reducer
