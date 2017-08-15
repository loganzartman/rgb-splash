Vue.component("color-picker", {
	template: `
		<div class="mdl-grid">
		<span class="mdl-cell mdl-cell--9-col-desktop mdl-cell--12-col mdl-cell--middle">
			<table style="width: 100%; border-spacing: 0; border-radius: 4px;">
				<tr v-for="(v, index) of value">
					<!-- Label -->
					<td style="width: 5px;">
						<span style="padding: .5em 0em; display: inline-block" v-bind:style="makeColor(index)">
							{{["RED", "GREEN", "BLUE"][index]}}
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

		<span class="mdl-cell mdl-cell--3-col-desktop mdl-cell--12-col mdl-shadow--3dp"
		 v-bind:style="mixedColor" style="height: inherit; min-height: 108px; border-radius: 4px;"></span>
		</div>`,
	props: ["value"],
	data: function(){
		return {
			value: [0,0,0]
		}
	},
	computed: {
		mixedColor: function() {
			return {"backgroundColor": `rgb(\
				${Math.floor(this.value[0]*255)},\
				${Math.floor(this.value[1]*255)},\
				${Math.floor(this.value[2]*255)}\
			)`};
		}
	},
	methods: {
		makeColor: function(channel) {
			let col = ['rgba(244,67,54,0.5)','rgba(76,175,80,0.5)','rgba(33,150,243,0.5)'][channel];
			return {
				color: col,
				fontWeight: "700"
			}
		}
	},
	watch: {
		value: function(newValue) {
			this.$emit("input", newValue);
		}
	}
});