Vue.component("slider-plus", {
	template: `
	<table style="border-spacing: 0; width: 100%;">
		<tr>
			<td>{{label}}</td>
			<td style="width: 100%;" ref="slContainer">
				<input type="range" class="mdl-slider mdl-js-slider" :min="min" :max="max" :step="step" v-on:input="sliderInput"/>
			</td>
			<td>
				<div class="mdl-textfield mdl-js-textfield" ref="tfContainer" style="width: 80px;">
					<input class="mdl-textfield__input" type="text" v-on:input="textInput" pattern="-?[0-9]*(\.[0-9]+)?">
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
		sliderInput: function(val) {
			let x = this.inputHandler(val);
			this.setText(x);
		},
		textInput: function(val) {
			let x = this.inputHandler(val);
			this.setSlider(x);
		},
		inputHandler: function(x) {
			let numeric = Number.parseFloat(x);
			if (!Number.isNaN(numeric)) {
				this.v = numeric;
				this.$emit("input", numeric);
				return numeric;
			}
			return this.v;
		},
		setSlider: function(val) {
			let slider = this.$refs.slContainer.getElementsByTagName("input")[0];
			slider.MaterialSlider.change(val);
		},
		setText: function(val) {
			let field = this.$refs.tfContainer;
			field.MaterialTextfield.change(val);
		}
	},
	watch: {
		value: function(newValue) {
			this.v = newValue;
			this.setSlider(newValue);
			this.setText(newValue);
		}
	}
});