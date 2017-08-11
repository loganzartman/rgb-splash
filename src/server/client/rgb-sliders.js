Vue.component("rgb-sliders", {
	template: `
	<div class="mdl-grid">
		<span class="mdl-cell mdl-cell--4-col-desktop mdl-cell--12-col mdl-cell--middle" 
		 v-for="(v, index) of value">
			<table style="width: 100%; border-collapse: collapse;"
			 v-bind:style="{backgroundColor: ['rgba(244,67,54,0.25)','rgba(76,175,80,0.25)','rgba(33,150,243,0.25)'][index]}">
				<tr>
					<!-- Label -->
					<td style="width: 40px;">
						<span class="color-chip" style="width: 40px;" >
							{{["Red", "Green", "Blue"][index]}}
						</span>
					</td>

					<!-- Slider -->
					<td style="width: auto;">
						<input class="mdl-slider mdl-js-slider" v-bind:id="'rgb'.charAt(index)+'-slider'"
				 		 v-model.number="value[index]" type="range" min="0" max="1" step="0.001"/>
					</td>
				</tr>
			</table>
		</span>
	</div>`,
	data: function(){
		return {
			value: [0,0,0]
		}
	},
	watch: {
		value: function(newValue) {
			this.$emit("input", newValue);
		}
	}
});