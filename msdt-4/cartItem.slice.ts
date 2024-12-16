import { CartItemsType, ProductType, Sizes } from '@/@types/mainTypes.types'
import { createSlice, PayloadAction } from '@reduxjs/toolkit'

const initialState: CartItemsType[] = []
const cartItemSlice = createSlice({
	name: 'store/cartItems',
	initialState,
	reducers: {
		addCartItem: (
			state,
			{ payload }: PayloadAction<{ product: ProductType; size: Sizes }>
		) => {
			const isExists = state.some(
				item =>
					item.cartItem.id === payload.product.id && item.size === payload.size
			)
			console.log(
				`${new Date()} The product was ${
					!isExists && 'not'
				} found in the shopping cart`
			)
			const id = state.findIndex(
				item =>
					item.cartItem.id === payload.product.id && item.size === payload.size
			)
			if (isExists) {
				if (state[id].count >= 10) {
					console.log(
						`${new Date()} The product has not been added to the shopping cart`
					)
					return
				} else {
					state[id].count++
					console.log(
						`${new Date()} The product has been added to the shopping cart`
					)
				}
			} else {
				state.push({ cartItem: payload.product, count: 1, size: payload.size })
				console.log(
					`${new Date()} The product has been added to the shopping cart`
				)
			}
		},
		removeCartItem: (
			state,
			{ payload }: PayloadAction<{ product: ProductType; size: Sizes }>
		) => {
			const isExists = state.some(
				item =>
					item.cartItem.id === payload.product.id && item.size === payload.size
			)
			console.log(
				`${new Date()} The product was ${
					!isExists && 'not'
				} found in the shopping cart`
			)
			const id = state.findIndex(
				item =>
					item.cartItem.id === payload.product.id && item.size === payload.size
			)
			if (!isExists) return
			state.splice(id, 1)
			console.log(
				`${new Date()} The product has been removed from the shopping cart`
			)
		},
		setCartItems(state, { payload }: PayloadAction<CartItemsType[]>) {
			state.splice(0, state.length)
			console.log(`${new Date()} The products have been added to the cart`)
			payload.map((e, i) => (state[i] = e))
		},
		setCartItem(state, { payload }: PayloadAction<CartItemsType>) {
			const isExists = state.some(
				item =>
					item.cartItem.id === payload.cartItem.id && item.size === payload.size
			)
			console.log(
				`${new Date()} The product was ${
					!isExists && 'not'
				} found in the shopping cart`
			)
			const id = state.findIndex(
				item =>
					item.cartItem.id === payload.cartItem.id && item.size === payload.size
			)
			if (!isExists) return
			state[id] = payload
			console.log(`${new Date()} The product have been added to the cart`)
		},
	},
})
export const { setCartItems, addCartItem, removeCartItem, setCartItem } =
	cartItemSlice.actions
export default cartItemSlice.reducer
