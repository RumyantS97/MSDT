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
		console.log(`${new Date()} GET ${$api}/${path}`)
		$api
			.get<AttributeResponse>(path)
			.then(response => {
				console.log(
					`${new Date()} the attribute array was successfully received`
				)
				return response.data.map(val => {
					return val.name
				})
			})
			.catch(error => {
				console.log(
					`${new Date()} Request to ${$api}/${path} failed with ${error.code}`
				)
				console.log(`${new Date()} the attribute array was not received`)
				return []
			})
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
			console.log(
				`${new Date()} filling in the attribute array has been completed`
			)
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
			console.log(
				`${new Date()} filling in the attribute array was completed with an error`
			)
		})
	},
})
export const { setAttribute } = attributeSlice.actions
export default attributeSlice.reducer
