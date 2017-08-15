Vue.component("slider-plus", {
	template: `
	<table style="border-spacing: 0; width: 100%;">
		<tr>
			<td>{{label}}</td>
			<td style="width: 100%;">
				<input type="range" class="mdl-slider mdl-js-slider" :min="min" :max="max" :step="step" v-model.number="v"/>
			</td>
			<td>
				<div class="mdl-textfield mdl-js-textfield" style="width: 80px;">
					<input class="mdl-textfield__input" type="text" v-model.number="v" pattern="-?[0-9]*(\.[0-9]+)?">
				</div>
			</td>
		</tr>
	</table>
	`,
	props: ["value", "label", "min", "max", "step"],
	data: function(){
		return {
			v: this.value
		}
	},
	methods: {
	},
	watch: {
		v: function(newValue) {
			this.$emit("input", newValue);
		}
	}
});