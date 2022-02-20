from __future__ import annotations


import os

import pandas as pd
import streamlit as st


st.set_page_config(layout="wide")


class Pager:
	"""Generates cycled stepper indices."""

	def __init__(self, count) -> None:
		self.count = count
		self.current = 0

	@property
	def next(self) -> int:
		"""Fetches next index."""
		n = self.current + 1
		# Cycles to beginning.
		if n > self.count-1:
			n -= self.count
		return n

	@property
	def prev(self) -> int:
		"""Fetches previous index."""
		n = self.current - 1
		# Cycles to end.
		if n < 0 :
			n += self.count
		return n

	def set_current(self, current) -> None:
		"""Sets current index."""
		self.current = current


def get_all_indices() -> list:
	"""Collects all index strings from data dir."""
	contents = os.listdir(datapath)
	gifs = [file for file in contents if file.endswith('.gif')]
	return [name.split('.')[0].split('_')[-1] for name in gifs]


def populate(index: str) -> None:
	"""Populates image data in separate columns."""
	with col_raw:
		st.subheader("Raw")
		st.image(f'{datapath}/raw_{index}.png')

	with col_ann:
		st.subheader("Annotated")
		st.image(f'{datapath}/annotated_{index}.png')

	with col_gif:
		st.subheader("GIF")
		st.image(f'{datapath}/anim_{index}.gif')


with st.sidebar:
	datapath = st.text_input(
		'Path to data:', 
		f'{os.getcwd()}/data')

indices = get_all_indices()
pager = Pager(len(indices))

st.title("IVUS Label Review for Ohio-Health")
col_raw, col_ann, col_gif = st.columns(3)

if "page" not in st.session_state:
    st.session_state["page"] = 0


with st.sidebar:
	st.write(f'Number of sets = {len(indices)}')
	default_goto = '<select>'
	options_goto = indices.copy()
	options_goto.insert(0, default_goto)
	index_goto = st.selectbox(
		'Go to:',
		tuple(options_goto)
		)
	if index_goto != default_goto:
		st.session_state['page'] = indices.index(index_goto)


if st.button("< Previous"):
	pager.set_current(st.session_state['page'])
	st.session_state['page'] = pager.prev

if st.button("Next >"):
	pager.set_current(st.session_state['page'])
	st.session_state['page'] = pager.next


st.write(f'Viewing index: {indices[st.session_state["page"]]}')
populate(indices[st.session_state['page']])

col_ann.radio('Eval:', ['Good', 'Bad'])
col_gif.text_input('Comments: ')
